from flask import Flask,blueprints,render_template

webhook_router = blueprints("webhook",__name__)


@webhook_router.route("/success")
def success():
    return render_template("success.html")

@webhook_router.route("/cancel")
def cancelled():
    return render_template("cancel.html")