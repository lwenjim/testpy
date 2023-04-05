# -*- coding:utf-8 -*-
import hashlib

import pymysql
import requests
import json
import math


class school_handle:
    # 成员变量
    cursor = ""
    connect = ""
    key = "yx_2020_express_dl"

    # mysql 配置
    host = "106.14.172.5"
    port = 3306
    user = "db_admin"
    passwd = "projectx2015"
    db = "yx_test_data"
    charset = 'utf8'

    def __init__(self):
        self.connect = self.get_mysql()
        self.cursor = self.connect.cursor()

    # 接口验签方法
    def get_sign(self, query):
        sign = query + self.key
        m = hashlib.md5()
        m.update(sign.encode("utf8"))
        sign = m.hexdigest()
        return sign

    # 获得数据库实例对象
    def get_mysql(self):
        return pymysql.Connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset=self.charset
        )

    def get_schools_data(self):
        sql_count = "select count(*) cnt from schools where city_id is not null"
        self.cursor.execute(sql_count)
        [count] = self.cursor.fetchone()
        if count <= 0 or self.cursor.rowcount <= 0:
            return
        page_size = 100
        pages = math.ceil(count / page_size)
        for page in range(1, pages):
            index = (page - 1) * page_size
            sql = "select * from schools where city_id is not null limit %s,%s" % (index, index + page_size)
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                yield row

    def api_express_school_list(self, city_id, school_name):
        query_string = 'cityId=%s&schoolName=%s' % (str(city_id), school_name)
        request_url = 'http://exp.classba.cn/api/express/schoolList?%s&sign=%s' % (
            query_string, self.get_sign(query_string))
        response = requests.get(request_url)
        return json.loads(response.text)

    def handle(self):
        for row in self.get_schools_data():
            city_id = row[5]
            school_name = row[1]
            primary_key = str(row[0])
            schools = self.api_express_school_list(city_id, school_name)
            if schools['code'] != 200:
                print("公校名称为：%s的记录调用接口异常\n" % school_name)
                continue
            if 'data' not in schools.keys() or len(schools['data']) == 0:
                print("公校名称为：%s的记录接口返回数据为空\n" % school_name)
                continue
            for school in schools['data']:
                sql = "update schools set school_id=%s where id=%s" % (school['id'], primary_key)
                if self.cursor.execute(sql) <= 0:
                    print("公校名称为：%s的记录回写数据库失败\n" % school_name)
                    continue
                self.connect.commit()
                if self.cursor.rowcount <= 0:
                    print("公校名称为：%s的记录回写数据库失败(可能已经更新过)\n" % school_name)
                    continue
                print("公校名称为：%s的记录处理成功\n" % school_name)
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    school_handle().handle()
