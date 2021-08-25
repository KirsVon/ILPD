from typing import List
from app.main.entity.cargo import Cargo
from app.main.entity.load_plan import LoadPlan
from app.main.entity.car import Car
from app.main.controller.config_name_management import curr_config_class


def get_load_plan_by_virtual_car(cargo_list: List[Cargo]) -> LoadPlan:
    """
    1. 通过货物列表/货物产生虚拟车辆
    2. 通过虚拟车辆创建装车清单
    3. 使用货物列表补充装车清单
    """
    # 1
    car_init_dict = cargo_list[0].as_dict()
    # 补充字段
    car_init_dict['license_plate_number'] = '0'  # config[curr_config_class].VIRTUAL_CAR_LICENSE
    car_init_dict['load_capacity'] = curr_config_class.MAX_LOAD_CAPACITY
    car_init_dict['create_time'] = cargo_list[0].can_send_date

    virtual_car = Car()
    virtual_car.set_attr(car_init_dict)
    # 2
    load_plan = LoadPlan(virtual_car)
    # 3
    if len(cargo_list) >= 1:
        # 补充装车清单
        for cargo in cargo_list:
            if isinstance(cargo, Cargo):
                success = load_plan.add(cargo)
            else:
                success = load_plan.add(Cargo(cargo))
            if success < 0:
                load_plan.cargo_list.append(cargo)
                load_plan.load += cargo.c_weight
                load_plan.is_full = True
                load_plan.unloading_address_list.add(cargo.unloading_address)
                load_plan.stock_list.add(cargo.out_stock)
                load_plan.commodity_list.add(cargo.commodity)
    return load_plan


def get_load_plan_by_car(car) -> LoadPlan:
    """
    通过虚拟车辆创建装车清单
    """
    load_plan = LoadPlan(car)
    return load_plan
