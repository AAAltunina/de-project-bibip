from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os
from decimal import Decimal
from datetime import datetime



class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        model_file = os.path.join(self.root_directory_path,'models.txt')
        with open(model_file, 'a') as f:
            f.write(f'{model.id};{model.name};{model.brand}\n')
        
        model_index_file = os.path.join(self.root_directory_path,'models_index.txt')
        with open(model_file, 'r') as f:
            line = f.readlines()

        with open(model_index_file, 'w') as mi:    
            for key, value in enumerate(line):
                model_id = value.split(';')[0]
                mi.write(f'{model_id};{key}\n')

        return model  


        

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        car_file = os.path.join(self.root_directory_path,'cars.txt')
        with open(car_file, 'a') as f:
            f.write(f'{car.vin};{car.model};{car.price};{car.date_start};{car.status}\n')

        index_file = os.path.join(self.root_directory_path,'cars_index.txt')
        
        with open(car_file, 'r') as f:
            line = f.readlines()

        with open(index_file, 'w') as inf:
            for key, value in enumerate(line):
                car_id = value.split(';')[0]
                inf.write(f'{car_id};{key}\n')

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        sell_file = os.path.join(self.root_directory_path, 'sales.txt')

        with open(sell_file, 'a') as f:
            f.write(f'{sale.sales_number};{sale.car_vin};{sale.sales_date};{sale.cost}\n')

        index_sell_file = os.path.join(self.root_directory_path, 'sales_index.txt')    

        with open(sell_file, 'r') as f:
            line = f.readlines()

        with open(index_sell_file, 'w') as isf:
            for key, value in enumerate(line):
                sell_id = value.split(';')[0]
                isf.write(f'{sell_id};{key}\n')
       
        #  создаю список в котором есть vin проданных авто
        sale_vin = []
        with open(sell_file, 'r') as f:
            line_sale = f.readlines()
            for element in line_sale:
                sale_vin.append(element.split(';')[1]) 
        
        # я открываю файл с машинами 
        car_file = os.path.join(self.root_directory_path,'cars.txt') 
        with open(car_file, 'r') as f:
            line_car = f.readlines() 
            new_line_car = [] 
            sold_car = None
            for element_car in line_car: 
                a = element_car.strip().split(';')
                if a[0] in sale_vin:
                    a[-1] = 'sold'
                    sold_car = Car(
                        vin=a[0],
                        model=int(a[1]),
                        price=Decimal(a[2]),
                        date_start=datetime.strptime(a[3], '%Y-%m-%d %H:%M:%S'),
                        status=CarStatus(a[4]))
            
                new_line_car.append(';'.join(a) + '\n')

        with open(car_file, 'w') as f:
            f.writelines(new_line_car)

        return sold_car
                
    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:

        car_file = os.path.join(self.root_directory_path,'cars.txt')
        result = []
        with open(car_file, 'r') as f:
            car = f.readlines()
            for element in car:
                new_element = element.strip().split(';')
                if new_element[4] == 'available':
                    result.append(Car(
                                vin=new_element[0],
                                model=int(new_element[1]),
                                price=Decimal(new_element[2]),
                                date_start=datetime.strptime(new_element[3], '%Y-%m-%d %H:%M:%S'),
                                status=CarStatus(new_element[4])))

        return result    



    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        model_file = os.path.join(self.root_directory_path,'models.txt')

        car_file = os.path.join(self.root_directory_path,'cars.txt') 

        sell_file = os.path.join(self.root_directory_path, 'sales.txt')

        with open(car_file, "r") as f1:
            cars_line = f1.readlines()

        car_info = None   
        for cars_element in cars_line: 
            a = cars_element.strip().split(';')
            if a[0] == vin:
                car_info = a
                model = a[1]

                break
        if car_info is None:    
            return None

        with open(model_file, "r") as f2:
            model_line = f2.readlines()

        model_info = None    
        for model_element in model_line:
            b = model_element.strip().split(';')
            if model == b[0]:  
                model_info = b    
                break  

        if  model_info is None:
            return None 

        
        sales_info = None  
        if os.path.exists(sell_file):     
            with  open(sell_file, "r") as f3: 
                sale_line = f3.readlines()

                for sale_element in sale_line:
                    s = sale_element.strip().split(';')
                    if vin == s[1]:
                        sales_info = s
                        break
        if sales_info is not None:
            sales_date = sales_info[2]
            sales_cost = sales_info[3]

        else:
            sales_date = None
            sales_cost = None 

            
        return CarFullInfo( 
            vin =  car_info[0], 
            car_model_name = model_info[1],
            car_model_brand = model_info[2], 
            price = car_info[2],
            date_start = car_info[3] ,
            status = CarStatus(car_info[4]), 
            sales_date = sales_date,
            sales_cost = sales_cost )

           
      
            
    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:

        car_file = os.path.join(self.root_directory_path,'cars.txt')
        
        car = None
        new_info_cars = []
        with open(car_file, 'r+') as f:
            cars_line = f.readlines()
            f.seek(0)

            for cars_element in cars_line: 
                a = cars_element.strip().split(';')
                if vin == a[0]:
                    a[0] = new_vin
                    new_info_cars.append(";".join(a) + "\n")
                    car = Car(
                        vin = a[0],
                        model = a[1],
                        price = a[2],
                        date_start = a[3],
                        status = CarStatus(a[4]),)
                else:
                    new_info_cars.append(cars_element) 

            f.writelines(new_info_cars)
            f.truncate()   
            
        index_file = os.path.join(self.root_directory_path,'cars_index.txt')

        new_info_index = []       
        with open(index_file, 'r+') as f:
            index_line = f.readlines() 
            f.seek(0)

            for index_element in index_line:
                i = index_element.strip().split(';')
                if i[0] == vin:
                    i[0] = new_vin
                    new_info_index.append(";".join(i) + "\n")
                else:
                    new_info_index.append(index_element)    
        
            f.writelines(new_info_index) 
            f.truncate()

        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        sell_file = os.path.join(self.root_directory_path, 'sales.txt')
        with open(sell_file, 'r') as f:
            sale_lines = f.readlines()

        new_sell = []

        for element in sale_lines:
            line = element.strip().split(';')
            if line[0] == sales_number: 
                vin_delete = line[1]
                continue
            new_sell.append(element) 

        with open(sell_file, 'w') as f:
            f.writelines(new_sell) 

        index_sell_file = os.path.join(self.root_directory_path, 'sales_index.txt') 
        with open(index_sell_file, 'r') as f:
            index_lines = f.readlines()

        new_index_file = []

        for element in index_lines:
            line = element.strip().split(';')
            if line[0] == sales_number: 
                continue
            new_index_file.append(element) 

        with open(index_sell_file, 'w') as f:
            f.writelines(new_index_file)
        
        car_file = os.path.join(self.root_directory_path,'cars.txt')
        with open(car_file, 'r+') as f:
            car_lines = f.readlines()
            f.seek(0)

            new_car_file = []
            car = None
            for element in car_lines:
                c = element.strip().split(';')
                if c[0] == vin_delete:
                    c[4] = 'available'
                    element = ";".join(c) + "\n"
                    car = Car(
                        vin=c[0],
                        model=c[1],
                        price=c[2],
                        date_start=c[3],
                        status=CarStatus.available
                )
                       
                new_car_file.append(element) 

            f.writelines(new_car_file)
            f.truncate()
        return car    
        

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        info = {}
         
        result = []
        
        model_file = os.path.join(self.root_directory_path,'models.txt')
        with open(model_file, 'r') as f:
            model_lines = f.readlines()

            for element in model_lines:
                m = element.strip().split(';')
                model_id = m[0]
                info[model_id] = 0

        car_file = os.path.join(self.root_directory_path,'cars.txt') 

        with open(car_file, 'r') as f:
            car_lines = f.readlines()         
            for element in car_lines:
                a = element.strip().split(';')
                model_id = a[1]
                if a[4] == 'sold':
                    info[model_id] += 1

        sell_info = {} 

        sell_file = os.path.join(self.root_directory_path, 'sales.txt')
        with open(sell_file, 'r') as f:
            sale_lines = f.readlines()

        for car_element in car_lines: 
            a = car_element.strip().split(';')
            vin_car = a[0]
            model_id = a[1]
            for sale_element in sale_lines:
                s = sale_element.strip().split(';')
                vin_sale = s[1]
                cost = s[3]
                if vin_car == vin_sale:
                    sell_info[model_id] = cost        
        
        sorted_models = sorted(info.items(), key=lambda x: (-x[1], -int(sell_info.get(x[0],0))))[:3]
       
        for model_id, sales_count in sorted_models:
            for line in model_lines:
                m = line.strip().split(';')
                if m[0] == model_id:
                    result.append(ModelSaleStats(
                        car_model_name=m[1],
                        brand=m[2],
                        sales_number=sales_count
                ))
                
        return result
    

