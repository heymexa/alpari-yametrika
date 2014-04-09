#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv
import re
import argparse

total = 0
supported_browsers = ['Google Chrome 26+', 'Firefox 25+', 'IE 11', 'IE 10', 'IE 9', 'Opera 12', 'Opera 18+']


def get_all_stats():
    global total
    total = 0
    result = {}
    try:
        with open(filename, encoding='utf8') as report_file:
            csv_file = csv.reader(report_file, delimiter=';', quotechar='"')
            for row in csv_file:
                os = row[0].strip()
                browser = re.split('^(.*?)\s([\d]+)', row[1].strip())
                visits = int(row[2])
                if len(browser) > 1:
                    if os not in result:
                        result[os] = {'total': 0, 'browsers': {}}
                    if browser[1] not in result[os]['browsers']:
                        result[os]['browsers'][browser[1]] = {}
                    if browser[2] not in result[os]['browsers'][browser[1]]:
                        result[os]['browsers'][browser[1]][browser[2]] = 0
                    result[os]['browsers'][browser[1]][browser[2]] += visits
                    result[os]['total'] += visits
                    total += visits
                else:
                    total += visits
            return result
    except FileNotFoundError:
        print('No such file or directory')
        exit()


def top10_os(html_flag):
    stats = get_all_stats()
    sorted_stats = sorted(list(stats.items()), key=lambda os: os[1]['total'], reverse=True)
    if html_flag:
        print(
            '<table class="standart" height="35" cellpadding="0" cellspacing="0" width="412"><thead><tr><th>&nbsp;№</th><th>OS<br></th><th>Кол-во <br></th></tr></thead><tbody>')
    for i in range(1, 11):
        os = sorted_stats[i - 1]
        if html_flag:
            print(
                '<tr><td style="text-align: center;">{0}</td><td> {1}</td><td style="text-align: center;">{2}%</td></tr>'.format(
                    i, os[0], '{0:.2f}'.format((os[1]['total'] / total) * 100)))
        else:
            print(str(i) + '.', os[0], "{0:.2f}".format((os[1]['total'] / total) * 100) + '%')
    if html_flag:
        print('</tbody></table>')


def top10_browsers(html_flag):
    result = {}
    stats = get_all_stats()
    for os in stats:
        browsers = stats[os]['browsers']
        for browser in browsers:
            for version in browsers[browser]:
                browser_name = get_browser_name(os, browser, version)
                if browser_name not in result:
                    result[browser_name] = 0
                result[browser_name] += browsers[browser][version]
    sorted_stats = sorted(result.items(), key=lambda os: os[1], reverse=True)
    i = 1
    total_supported_browsers = 0
    if html_flag:
        print(
            '<table class="standart" height="35" cellpadding="0" cellspacing="0" width="300"><thead><tr><th>&nbsp;№</th><th>Браузер<br></th><th>Кол-во <br></th></tr></thead><tbody>')
    for browser in sorted_stats:
        if i < 11 or browser[0] in supported_browsers:
            if html_flag:
                print(
                    '<tr><td style="text-align: center;">{0}</td><td style="padding-left: 5px">{1}</td><td style="text-align: center;">{2}%</td></tr>'.format(
                        i, browser[0], '{0:.2f}'.format((browser[1] / total) * 100)))
            else:
                print(str(i) + '.', browser[0], "{0:.2f}".format((browser[1] / total) * 100) + '%')
            total_supported_browsers += (browser[1] / total) * 100
        i += 1
    if html_flag:
        print(
            '<tr><td style="text-align: center;"></td><td> Others</td><td style="text-align: center;">{0}</td></tr></tbody></table>'.format(
                '{0:.2f}'.format(100 - total_supported_browsers) + '%'))
    else:
        print('Others:', "{0:.2f}".format(100 - total_supported_browsers) + '%')


def get_browser_name(os, browser, version):
    version = int(version)
    if browser == 'Firefox' and version >= 25:
        return 'Firefox 25+'
    if browser == 'Opera' and version >= 18:
        return 'Opera 18+'
    if browser == 'Opera' and version == 12:
        return 'Opera 12'
    if browser == 'Google Chrome' and version >= 26:
        return 'Google Chrome 26+'
    if browser == 'ChromeMobile' and version >= 26:
        return 'ChromeMobile 26+'
    if browser == 'Яндекс.Браузер' and version >= 13:
        return 'Яндекс.Браузер 13+'
    if browser == 'Android Browser' and version >= 4:
        return 'Android Browser 4+'
    if browser == 'Mobile Safari' and version >= 7:
        return 'Mobile Safari 7+'
    if browser == 'MSIE':
        return 'IE ' + str(version)
    return browser


def create_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('filename', help='path to the report file')
    arg_parser.add_argument('-b', '--browsers', action='store_const', const=True, help='show top10 browsers')
    arg_parser.add_argument('-o', '--os', action='store_const', const=True, help='show top10 OS')
    arg_parser.add_argument('-H', '--html', action='store_const', const=True, help='show result as html')

    return arg_parser


if __name__ == "__main__":
    parser = create_arg_parser()
    namespace = parser.parse_args()

    filename = namespace.filename
    html = namespace.html

    if namespace.os:
        top10_os(html)
    elif namespace.browsers:
        top10_browsers(html)
    else:
        top10_browsers(html)
