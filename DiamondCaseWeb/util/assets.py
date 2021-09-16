#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_assets import Environment, Bundle


def register_assets(app):
    assets = Environment(app)
    assets.url = app.static_url_path
    homepage_css = Bundle('style/homepage.scss', filters='pyscss',
                          output='generated_style/homepage.css')
    locator_css = Bundle('style/locator.scss', filters='pyscss',
                         output='generated_style/locator.css')
    about_css = Bundle('style/about.scss', filters='pyscss',
                       output='generated_style/about.css')
    contact_css = Bundle('style/contact.scss', filters='pyscss',
                         output='generated_style/contact.css')
    product_css = Bundle('style/product.scss', filters='pyscss',
                         output='generated_style/product.css')
    product_category_css = Bundle('style/product_category.scss',
                                  filters='pyscss',
                                  output='generated_style/product_category.css'
                                  )
    base_css = Bundle('style/base.scss', filters='pyscss',
                      output='generated_style/base.css')
    machine_product_css = Bundle('style/machine_product.scss',
                                 filters='pyscss',
                                 output='generated_style/machine_product.css'
                                 )
    cart_css = Bundle('style/cart.scss', filters='pyscss',
                      output='generated_style/cart.css')
    checkout_css = Bundle('style/checkout.scss', filters='pyscss',
                          output='generated_style/checkout.css')
    blog_css = Bundle('style/blog.scss', filters='pyscss',
                      output='generated_style/blog.css')
    help_css = Bundle('style/help.scss', filters='pyscss',
                      output='generated_style/help.css')
    term_css = Bundle('style/term.scss', filters='pyscss',
                      output='generated_style/term.css')

    assets.register('homepage_css', homepage_css)
    assets.register('locator_css', locator_css)
    assets.register('about_css', about_css)
    assets.register('contact_css', contact_css)
    assets.register('product_css', product_css)
    assets.register('product_category_css', product_category_css)
    assets.register('machine_product_css', machine_product_css)
    assets.register('cart_css', cart_css)
    assets.register('checkout_css', checkout_css)
    assets.register('blog_css', blog_css)
    assets.register('help_css', help_css)
    assets.register('term_css', term_css)
    assets.register('base_css', base_css)
