
import sys
import logging
import json
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host= "hublocker-dev.ccvodtkje6ie.af-south-1.rds.amazonaws.com",
    database="hublocker",
    user="owilson",
    password="owilson"
    # port="5432"
)


def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def currentTime(event, context):
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, the current time is " + str(current_time)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

# def lambda_handler(event, context):
#     #get request raw data
#     dataPart = event['body']

#     #Parse Raw Data
#     # rectifyData = parsingData(dataPart)

#     response = {
#         "statusCode": 200,
#         "statusCode": 200,
#         "body": json.dumps(dataPart),
#         "headers": {
#             "Content-Type": "application/json"
#         }
#     }

#     return response

# def parsingData(dataPart):

    # chucks = dataPart.split('\r\n')

def getAllPackageCountByStatus(event, context):
    try:
        cur = conn.cursor(cursor_factory = RealDictCursor)
        id = event['pathParameters']
        query = """
                    SELECT COUNT(*) FROM locker_service.tbl_package WHERE locker_service.tbl_package.package_status= %s
                """
        data = (id,)
        cur.execute(query,data)
        results = cur.fetchall()
        json_result = json.dumps(results)
        print(json_result)
        print(event['pathParameters'])
        # event['queryStringParameters']
        return dict(
            statusCode=200,
            body= { 
                'data': json_result,
                'event' :event,
                },
        )
    except Exception as e:
        return dict(
            statusCode=500,
            body=str(e),
        )

def getAllPackage(event, context):
    try:
        cur = conn.cursor(cursor_factory = RealDictCursor)
        # query ="SELECT user_id, package_start_time, package_end_time, locker_id, package_size, package_wght, dlvry_mthd, package_status, courier_id, created_at, updated_at FROM locker_service.tbl_package"
        query = """
            SELECT 
                package_id,user_id, package_start_time, package_end_time, locker_id, package_size, package_wght, dlvry_mthd, package_status, courier_id, created_at, updated_at 
            FROM 
                locker_service.tbl_package
            """
        cur.execute(query)
        results = cur.fetchall()
        json_result = json.dumps(results, indent=1, sort_keys=True,default=str)
        print(json_result)
        return dict(
            statusCode=200,
            body=json_result,
        )
    except Exception as e:
        return dict(
            statusCode=500,
            body=str(e),
        )
    
def savePackage(event, context):
    try:
        query = """
            INSERT INTO locker_service.tbl_package 
                (user_id, package_start_time, package_end_time, locker_id, package_size, package_wght, dlvry_mthd, package_status, courier_id)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """

        # query = """
        #     INSERT INTO locker_service.tbl_package (user_id, package_start_time, package_end_time, locker_id, package_size, package_wght, dlvry_mthd, package_status, courier_id) VALUES(1,'2023-10-20 09:30','2023-11-06 18:30',1,'0.3kg','1.2','1',4,1);
        #     """
        
        # event['queryStringParameters']['user_id']
        bodyData = json.loads(event['body'])

        user_id = bodyData['user_id']
        package_start_time = bodyData['package_start_time']
        package_end_time = bodyData['package_end_time']
        locker_id = bodyData['locker_id']
        package_size = bodyData['package_size']
        package_wght = bodyData['package_wght']
        dlvry_mthd = bodyData['dlvry_mthd']
        package_status = bodyData['package_status']
        courier_id = bodyData['courier_id']
        data = (user_id,package_start_time,package_end_time,locker_id,package_size,package_wght,dlvry_mthd,package_status,courier_id,)
        
        cur = conn.cursor()
        cur.execute(query,data)
        conn.commit()
        cur.close()


        # 2. Construct the body of the response object
        transactionResponse = {}
        # returning values originally passed in then add separate field at the bottom
        # transactionResponse['data'] = data
        transactionResponse['message'] = 'saved'

        # 3. Construct http response object
        response = {}
        response['statusCode'] = 200
        response['headers'] = {}
        response['headers']['Content-Type'] = 'application/json'
        response['body'] = json.dumps(transactionResponse)

        return response
        # return dict(
        #     statusCode=200,
        #     data=data,
        #     body='saved',
        # )
    except Exception as e:
        return dict(
            statusCode=500,
            body=str(e),
        )
