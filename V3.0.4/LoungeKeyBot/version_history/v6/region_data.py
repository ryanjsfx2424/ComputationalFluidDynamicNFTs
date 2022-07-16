import os
import glob
import json
class RegionData(object):
    def load_region_data(self):
        self.region_data = {}

        usa_data_path = "region_data/us_data"
        country_data_path = "region_data/country_data"

        self.region_data["c-america-carribean"] = self.load_region_data1(
            country_data_path + "/carribean.txt")

        self.region_data["c-america-carribean"] = self.load_region_data1(
            country_data_path + "/central_america.txt", 
            self.region_data["c-america-carribean"])

        self.region_data["south-america"] = self.load_region_data1(
            country_data_path + "/south_america.txt")

        self.region_data["europe"] = self.load_region_data2(
            country_data_path + "/europe.txt")

        self.region_data["mena"] = self.load_region_data3(
            country_data_path + "/middle_east.txt")

        self.region_data["mena"] = self.load_region_data3(
            country_data_path + "/north_africa.txt",
            self.region_data["mena"])

        self.region_data["africa"] = self.load_region_data4(
            country_data_path + "/west_africa.txt"
        )
        self.region_data["africa"] = self.load_region_data4(
            country_data_path + "/central_africa.txt",
            self.region_data["africa"]
        )
        self.region_data["africa"] = self.load_region_data4(
            country_data_path + "/south_africa.txt",
            self.region_data["africa"]
        )

        self.region_data["c-and-s-asia"] = self.load_region_data3(
            country_data_path + "/central_asia.txt"
        )
        self.region_data["c-and-s-asia"] = self.load_region_data3(
            country_data_path + "/south_asia.txt",
            self.region_data["c-and-s-asia"]
        )

        self.region_data["east-asia"] = self.load_region_data3(
            country_data_path + "/east_asia.txt"
        )

        self.region_data["oceania"] = self.load_region_data5(
            country_data_path + "/oceania.txt"
        )

        self.region_data["uk-and-ireland"] = ["uk","ireland"]
        self.region_data["canada"] = ["canada", "canadian"]

        self.region_data["usa"] = self.load_region_data6(
            usa_data_path + "/states.txt"
        )

        home_path = os.getcwd()
        os.chdir(usa_data_path)
        fs = glob.glob("*.txt")
        for fn in fs:
            if fn == "states.txt":
                continue
            # end if
            self.region_data[fn.replace(".txt","")] = \
                self.load_region_data7(fn)
        # end for

        with open("us_city_data.json", "r") as fid:
            self.region_data["us_city_map"] = json.loads(fid.read())
        # end with open

        os.chdir(home_path)
    # end load_region_data

    def load_region_data1(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            for line in fid:
                data.append(line.replace(" ","").replace("\n","").lower())
            # end for
        # end with
        return data
    # end load_region_data1

    def load_region_data2(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            for line in fid:
                data.append(line.split()[1].replace("*","").replace("\n","").lower())
            # end for
        # end with
        return data
    # end load_region_data2

    def load_region_data3(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            line = fid.read()
            countries = line.split(", ")
            for country in countries:
                data.append(country.replace(" ", "").replace("\n","").lower())
            # end for
        # end with
        return data
    # end load_region_data3

    def load_region_data4(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            for line in fid:
                data.append(line.split()[0].lower())
            # end for
        # end with
        return data
    # end load_region_data4

    def load_region_data5(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            for line in fid:
                data.append(line.split()[1].lower())
            # end for
        # end with
        return data
    # end load_region_data5

    def load_region_data6(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            for line in fid:
                data.append(line.split()[-1].strip(" \n").lower())
            # end for
        # end with
        return data
    # end load_region_data6

    def load_region_data7(self, fname, data = None):
        if data is None:
            data = []
        # end if

        with open(fname, "r") as fid:
            for line in fid:
                data.append(line.replace("\n",""))
            # end for
        # end with
        return data
    # end load_region_data7
# end class RegionData
## end region_data.py