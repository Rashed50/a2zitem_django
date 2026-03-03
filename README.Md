# Django Templates

## 1. Create Vertual Invironments

#### Windows 
```bash
py -m venv env
```
or,
```bash
py -3.13 -m venv env
```
#### Linux
```bash
python3 -m venv env
```


## 2. Activate Virtual Invironments

#### Windows 
```bash
env\Scripts\activate
```

#### Linux
```bash
source env/bin/activate
```



## 3. Deactivate Virtual Invironments

```bash
deactivate
```


## 4. Upgrade PIP

```bash
python.exe -m pip install --upgrade pip
```



## 5. Install Requirement Txt Files
```bash
pip install -r requirements.txt
```



## 6. Create and Copy .env file
```bash
copy .env.example .env
```


## 7. Makemigration
```bash
python manage.py makemigrations
```



## 8. Migrate
```bash
python manage.py migrate
```



## 9. Create Superuser
```bash
python manage.py createsuperuser
```
1. Superuser Users
```bash
python manage.py superuser 
```
- admin@test.com
- 123456ra

2. Staff Users
```bash
python manage.py staffuser
```
- staff@test.com
- 123456ra


## 10. Now can run the Django server 
```bash
python manage.py runserver
```

# === Tailwind CSS and Vue Install ===
## 11. Install Tailwind CSS
```bash
python manage.py tailwind install
```

## 12. Run Tailwind CSS
```bash
python manage.py tailwind start
```
```bash
python manage.py tailwind build
```

## 13. Vue JS Installation
```bash
cd frontend
```
```bash
npm install
```
```bash
yarn
```

## 14. Run Vue JS
```bash
npm run serve
```
```bash
yarn dev
```

# ======= Bulk Import =======
## 1. Supplier Bulk Import
```bash
python manage.py BulkSupplier
```

## 2. Brand Bulk Import
```bash
python manage.py BulkBrand
```

## 3. Category Bulk Import
```bash
python manage.py BulkCategory
```

## 4. Color Bulk Import
```bash
python manage.py BulkColor
```

## 5. Size Bulk Import
```bash
python manage.py BulkSize
```

## 6. Unit Of Measure Bulk Import
```bash
python manage.py BulkUnit
```