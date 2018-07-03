# -*-coding:utf-8-*-
import sys
import re
from itertools import groupby, dropwhile
from operator import itemgetter
from config.Configuration_of_rolling_top_words import cfg_rtw


def reduceByKey(fun, keygetter, data):
    return [(key, reduce(fun, map(lambda x: x[1], valuelist))) for key, valuelist in groupby(data, key=keygetter)]


def parse_producer(line):
    m = re.search(""".*hot word: '(\w*)', count:(\d*)""", line)
    return (m.group(1), int(m.group(2)))


def produce_producer_out(producer_out_filename, hotword_num_per_window, hotword_rate):
    with open(producer_out_filename, "r") as producer_out_file:
        p = filter(lambda x: 'hot word' in x, producer_out_file.readlines())
        pros = map(lambda x: parse_producer(x), p)
        pros.sort()
        pro_reduce = reduceByKey(lambda x, y: x + y, itemgetter(0), pros)
        theoretical_word_count_dict = dict(pro_reduce)
        pro_counts = map(lambda x: int(x[1]), pro_reduce)
        theoretical_hotword_num = len(pro_counts)
        theoretical_total_count_per_window = (sum(pro_counts) / float(
            theoretical_hotword_num)) * hotword_num_per_window * hotword_rate
        return (theoretical_hotword_num, theoretical_total_count_per_window, theoretical_word_count_dict)


def produce_consumer_out(consumer_out_filename_list):
    total_count_per_window_list = []
    for consumer_out_filename in consumer_out_filename_list:
        with open(consumer_out_filename, "r") as consumer_out_file:
            total_count_per_window_list += dropwhile(
                lambda total_count: total_count == 0,
                map(
                    lambda total_count_string: int(total_count_string),
                    filter(
                        lambda total_count_string: len(total_count_string) == 16,
                        map(
                            lambda match_object: match_object.group(1),
                            filter(
                                lambda match_object: match_object != None,
                                map(
                                    lambda line: re.search("""\+\+\+\+\+(\d*)-----""", line),
                                    consumer_out_file.readlines()))))))
    realistic_window_count = len(total_count_per_window_list)
    realistic_total_count_per_window = sum(total_count_per_window_list) / float(realistic_window_count)
    # print total_count_per_window_list
    # print realistic_window_count, realistic_total_count_per_window

    word_count_list = []
    for consumer_out_filename in consumer_out_filename_list:
        with open(consumer_out_filename, "r") as consumer_out_file:
            word_count_list += map(
                lambda word_count_string_pair: (
                str(int(word_count_string_pair[0])) + "testing", int(word_count_string_pair[1])),
                filter(
                    lambda word_count_string_pair: len(word_count_string_pair[0]) == 9 and len(
                        word_count_string_pair[1]) == 16,
                    map(
                        lambda match_object: (match_object.group(1), match_object.group(2)),
                        filter(
                            lambda match_object: match_object != None,
                            map(
                                lambda line: re.search("""#####(\d*)testing,(\d*)\*\*\*\*\*""", line),
                                consumer_out_file.readlines())))))
    word_count_list.sort()
    realistic_word_count_dict = dict(reduceByKey(lambda x, y: max(x, y), itemgetter(0), word_count_list))
    return (realistic_window_count, realistic_total_count_per_window, realistic_word_count_dict)


# def main():
#     theoretical_window_count = int(sys.argv[1])
#
#     hotword_num_per_window = int(sys.argv[2])
#     producer_out_filename = sys.argv[3]
#     consumer_out_filename_list = sys.argv[4:]
#
#     hotword_rate = 21 / 11.0
#
#     (theoretical_hotword_num, theoretical_total_count_per_window, theoretical_word_count_dict) = produce_producer_out(
#         producer_out_filename, hotword_num_per_window, hotword_rate)
#
#     (realistic_window_count, realistic_total_count_per_window, realistic_word_count_dict) = produce_consumer_out(
#         consumer_out_filename_list)
#
#     accuracy_list = filter(
#         lambda accuracy: accuracy <= 1,
#         map(
#             lambda (word, num): realistic_word_count_dict.get(word, 0) / float(num),
#             theoretical_word_count_dict.items()))
#     average_accuracy = sum(accuracy_list) / float(len(accuracy_list))
#     realistic_hotword_num = len(accuracy_list)
#     print int(theoretical_total_count_per_window), int(
#         realistic_total_count_per_window), theoretical_window_count, realistic_window_count, theoretical_hotword_num, realistic_hotword_num, "%.3f" % average_accuracy


def analyse_main(
        theoretical_window_count,
        hotword_num_per_window,
        producer_out_filename,
        consumer_out_filename
):
# def main():
#     theoretical_window_count = int(sys.argv[1])
#
#     hotword_num_per_window = int(sys.argv[2])
#     producer_out_filename = sys.argv[3]
#     consumer_out_filename_list = sys.argv[4:]

    hotword_rate = 21 / 11.0

    (theoretical_hotword_num, theoretical_total_count_per_window, theoretical_word_count_dict) = produce_producer_out(
        producer_out_filename, hotword_num_per_window, hotword_rate)

    (realistic_window_count, realistic_total_count_per_window, realistic_word_count_dict) = produce_consumer_out(
        [consumer_out_filename])

    accuracy_list = filter(
        lambda accuracy: accuracy <= 1,
        map(
            lambda (word, num): realistic_word_count_dict.get(word, 0) / float(num),
            theoretical_word_count_dict.items()))
    average_accuracy = sum(accuracy_list) / float(len(accuracy_list))
    realistic_hotword_num = len(accuracy_list)
    print "---- 打印最终分析结果 ----"
    print int(theoretical_total_count_per_window), int(
        realistic_total_count_per_window), theoretical_window_count, realistic_window_count, theoretical_hotword_num, realistic_hotword_num, "%.3f" % average_accuracy


if __name__ == '__main__':
    theoretical_window_count = cfg_rtw.exec_time * 1000 / cfg_rtw.slide_window_size
    hotword_num_per_window = cfg_rtw.window_size / cfg_rtw.interval
    producer_out_filename = cfg_rtw.local_log_base_path + "gen_data.log"
    consumer_out_filename = cfg_rtw.local_log_base_path + "worker.log"
    analyse_main(
        theoretical_window_count,
        hotword_num_per_window,
        producer_out_filename,
        consumer_out_filename
    )
