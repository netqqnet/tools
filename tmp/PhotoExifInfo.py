import exifread
import requests
class PhotoExifInfo():
    def __init__(self,photo_path):
        self.photo_path = photo_path
        self.baidu_map_ak = ""

    def get_tags(self):
        """获取照片信息"""
        img = open(self.photo_path, 'rb')
        tags = exifread.process_file(img)
        #打印照片其中一些信息
        print('拍摄时间：', tags['EXIF DateTimeOriginal'])
        print('照相机制造商：', tags['Image Make'])
        print('照相机型号：', tags['Image Model'])
        print('照片尺寸：', tags['EXIF ExifImageWidth'], tags['EXIF ExifImageLength'])
        img.close()
        return tags

    def get_lng_lat(self):
        """经纬度转换"""
        tags = self.get_tags()
        try:
            # 纬度
            LatRef = tags["GPS GPSLatitudeRef"].printable
            Lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            Lat = float(Lat[0]) + float(Lat[1]) / 60 + float(Lat[2]) / 3600
            if LatRef != "N":
                Lat = Lat * (-1)
            # 经度
            LonRef = tags["GPS GPSLongitudeRef"].printable
            Lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            Lon = float(Lon[0]) + float(Lon[1]) / 60 + float(Lon[2]) / 3600
            if LonRef != "E":
                Lon = Lon * (-1)
            return Lat,Lon
        except:
            print('Unable to get')

    def get_city_info(self):
        result = self.get_lng_lat()
        if result:
            Lat, Lon = result
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak="+self.baidu_map_ak+"&output=json&coordtype=wgs84ll&location=" + str(Lat) + ',' + str(Lon)
            response = requests.get(url).json()
            status = response['status']
            if status == 0:
                address = response['result']['formatted_address']
                return address
            else:
                print('baidu_map error')

if __name__ == '__main__':
    result = PhotoExifInfo("IMG_20190918_080329.jpg").get_city_info()
    print("拍摄地点：{}".format(result))