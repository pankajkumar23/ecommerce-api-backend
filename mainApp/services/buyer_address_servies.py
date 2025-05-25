from database.db import db
from models.address_model import Address


def add_address_services(data, user_data):
    try:
        id = user_data["id"]
        add_address = Address(address=data.address, country=data.country, city=data.city, state=data.state,user_id = id,postalcode=data.postalcode)
        db.session.add(add_address)
        db.session.commit()
        return {"message": "product sucessfully address added",
                "address":add_address.address,
                "country":add_address.country,
                "city":add_address.city,
                "state":add_address.state,
                "postalcode":add_address.postalcode,
                },200
    except Exception as e:
        print(f"Error at add_address_implementation{str(e)}")
        return f"message: {str(e)}", 400


def user_address_services( user_data):
    try:
        address_list = []
        id = user_data["id"]
        addresses = Address.query.filter_by(user_id=id).all()
        if addresses:
            for user_address in addresses:
                address_list.append(
                    {
                        "id": user_address.id,
                        "address": user_address.address,
                        "country": user_address.country,
                        "city": user_address.city,
                        "state": user_address.state,
                        "postalcode": user_address.postalcode,
                        
                    }
                )
        return {"user_id":id,"addresses": address_list}, 200
    except Exception as e:
        print(f"Error at user_address_implementation{str(e)}")
        return f"message: {str(e)}", 400


def update_address_services(data, user_data, id):
    try:
        if not id:
           return {"message":"id not found"},404
        user_id = user_data["id"]
        addresses= Address.query.filter_by(user_id=user_id).all()
        for address in addresses:
            if address.id == id:
                update_address = Address.query.get(id)
                if data.address:
                    update_address.address = data.address
                    update_address.country = data.country
                    update_address.state = data.state
                    update_address.city = data.city
                    update_address.postalcode = data.postalcode
                elif data.country:
                    update_address.country = data.country
                elif data.state:
                    update_address.state = data.state
                elif data.city:
                    update_address.city = data.city
                elif data.postalcode:
                    update_address.postalcode = data.postalcode
                db.session.commit()
                return {
                    "message": "address sucessfully updated",
                    "address": update_address.address,
                    "country": update_address.country,
                    "city": update_address.city,
                    "state": update_address.state,
                    "postalcode": update_address.postalcode,
                }, 200
        return {"message":"address not found"},401
    except Exception as e:
        print(f"Error at update_address_implementation{str(e)}")
        return f"message: {str(e)}", 400
