import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-attendance-system-caf12-default-rtdb.asia-southeast1.firebasedatabase.app/"
})


ref = db.reference('Students')

data = {
    "05917711921":
        {
            "name": "Samyak Sharma",
            "id":"05917711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 10:24:34",
            "attendance": 0
        },
    "05517711921":
        {
            "name": "kalpana",
            "id":"05517711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 10:04:34",
            "attendance":0
        },
    "01417711921":
        {
            "name": "Anshika Jain",
            "id":"01417711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 12:34:34",
            "attendance": 0
        },
    "03717711921":
        {
            "name": "Ribhav Bhatia",
            "id":"03717711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 12:34:34",
            "attendance": 0
        },
    "04017711921":
        {
            "name": "Mansha Rathee",
            "id":"04017711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 12:34:34",
            "attendance": 0
        },
    "02917711921":
        {
            "name": "Mehul Batra",
            "id":"02917711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 12:34:34",
            "attendance": 0
        },
    "04317711921":
        {
            "name": "Shivam Sharma",
            "id":"04317711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 12:34:34",
            "attendance": 0
        },
    "02417711921":
        {
            "name": "Prakhar Jain",
            "id":"02417711921",
            "Branch": "AIDS-A",
            "Year": "2",
            "last_attendance_time": "2023-6-16 12:34:34",
            "attendance": 0
        }
}

for key,value in data.items():
    ref.child(key).set(value)