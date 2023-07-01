class Result():

    def __init__(self, count, result_list, specialty_dict, edu_req_dict, major_req_dict):
        self.count = int(count)
        self.result_list = result_list
        self.specialty_dict = specialty_dict
        self.edu_req_dict = edu_req_dict
        self.major_req_dict = major_req_dict

    def __str__(self):
        return f'{self.count}, {self.result_list}, {self.specialty_dict}, {self.edu_req_dict}, {self.major_req_dict}'

    def integrate(self, target):
        self.count += int(target.count)
        self.result_list.extend(target.result_list)

        for key, value in target.specialty_dict.items():
            if key in self.specialty_dict:
                self.specialty_dict[key] += int(value)
            else:
                self.specialty_dict[key] = int(value)

        for key, value in target.edu_req_dict.items():
            if key in self.edu_req_dict:
                self.edu_req_dict[key] += int(value)
            else:
                self.edu_req_dict[key] = int(value)

        for key, value in target.major_req_dict.items():
            if key in self.major_req_dict:
                self.major_req_dict[key] += int(value)
            else:
                self.major_req_dict[key] = int(value)


if __name__ == '__main__':
    a = Result(0, [1], {'a': 1}, {}, {})
    b = Result(3, [5, 8], {'a': 5, 'b': 6}, {'tt': 3}, {'lala': 9})
    a.integrate(b)
    print(a)
