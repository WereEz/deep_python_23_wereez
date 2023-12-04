import time
import random
import json
import cjson
import ujson
import faker


def dumps_time_tests(data):
    print("Время выполнения dumps")
    start = time.time()
    for person in data:
        res = json.dumps(person)
    end = time.time()
    print(f"время для JSON: {end - start} sec")

    start = time.time()
    for person in data:
        res = cjson.dumps(person)
    end = time.time()
    print(f"время для CJSON: {end - start} sec")

    start = time.time()
    for person in data:
        res = ujson.dumps(person)
    end = time.time()
    print(f"время для UJSON: {end - start} sec")


def loads_time_tests(json_list):
    print("Время выполнения loads")

    start = time.time()
    for JSON in json_list:
        res = json.loads(JSON)
    end = time.time()
    print(f"время для JSON: {end - start} sec")

    start = time.time()
    for JSON in json_list:
        res = cjson.loads(JSON)
    end = time.time()
    print(f"время для CJSON: {end - start} sec")

    start = time.time()
    for JSON in json_list:
        res = ujson.loads(JSON)
    end = time.time()
    print(f"время для UJSON: {end - start} sec")


def main():
    data = []
    json_list = []

    fake = faker.Faker()
    for _ in range(100000):
        person = {
            "name": fake.name(),
            "age": random.randint(20, 50),
            "city": fake.city(),
            "email": fake.email(),
            "passport_number": str(fake.random_int(min=0000000000, max=9999999999)),
            "phone_number": f"+7{random.randint(9000000000, 9999999999)}",
        }
        data.append(person)
        json_list.append(json.dumps(person))

    dumps_time_tests(data)
    loads_time_tests(json_list)


if __name__ == "__main__":
    main()
