import pandas as ps
import datetime
import time

class calc:
    def __init__(self):
        self.debug = False
        self.start()


    def start(self):

        self.gender = input("Enter gender(Format m or f): ")
        self.read_data()
        self.user_prompt()
        self.calculate()

    def read_data(self):
        if(self.gender == 'm'):
            self.data = ps.read_csv("male_by_countries.csv",skiprows=4)
        if(self.gender == 'f'):
            self.data = ps.read_csv("female_by_countries.csv",skiprows=4)
        #print(self.data['Country_Name'])
    def user_prompt(self):
        print("It's average life calculator! Year supported: 1960-2016")
        if self.debug:
            self.gender = 'm'
            self.country = 'Italy'
            self.year = '1997'
            self.option = '1'
        else:

            print("----------------List of countries---------------------")
            time.sleep(0.5)
            for i in self.data['Country_Name']:
                print(i)
                time.sleep(0.05)
            print("------------------------------------------------------")
            self.country = input("Enter full country name with capital letter in the beginning(e.g Russian Federation): ")
            self.birthday_str = input("Enter birthday data(Format dd/mm/year. e.g: 11/12/1997): ")
            self.option = input("Enter output option(1-Days 2-Hours 3-Minutes): ")
            self.bd_arr = self.birthday_str.split('/')
            self.year = self.bd_arr[2]
            self.month = self.bd_arr[1]
            self.day = self.bd_arr[0]

    def calculate(self):
            data = self.data[self.data.Country_Name == self.country][[self.year]]
            exp_years = data[self.year][data.index[0]]
            print("Your average lifetime is: {}".format(exp_years))
            d0 = datetime.date(int(self.year),int(self.month), int(self.day))
            d1 = datetime.datetime.now().date()
            years = (d1-d0).days/365
            print("You are now {} years".format(years))
            if(self.option == '1'):
                print("In days you are {}".format((d1-d0).days))
                print("In days time is left for you is: {}".format((exp_years - years)*365))
            elif(self.option == '2'):
                print("In hours you are {}".format((d1-d0).days*24))
                print("In hours time is left for you is: {}".format((exp_years - years)*365*24))
            elif(self.option == '3'):
                print("In minutes you are {}".format((d1-d0).days*24*60))
                print("In minutes time is left for you is: {}".format((exp_years - years)*365*24*60))

if __name__ == '__main__':
    c = calc()
