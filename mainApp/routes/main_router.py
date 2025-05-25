from flask import Flask, Blueprint
from routes.user_router import user_router
from routes.seller_router import seller_router
from routes.admin_router import admin_router
from routes.buyer_router import buyer_router
from routes.webhook_router import webhook_router

main_router = Blueprint("v1", __name__)
main_router.register_blueprint(user_router)
main_router.register_blueprint(seller_router)
main_router.register_blueprint(buyer_router)
main_router.register_blueprint(admin_router)
main_router.register_blueprint(webhook_router)