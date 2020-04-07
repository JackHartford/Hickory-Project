{
    'name': 'Hickory Web Login',
    'category': 'Website',
    'sequence': 55,
    'license': 'OEEL-1',
    'summary': 'Hickory: Website Customization',
    'website': 'https://www.odoo.com/page/e-commerce',
    'version': '1.0',
    'description': """
Hickory: Loign Page Cutomization
================================
* Login Page Button Cutomization
* On the login page, do the following:
    * deleted the "Log In" button
    * put "Log in with Google" as the top button
    * "Don't have an account?" as the 2nd button below this, change the text to say "Create an account"
    * "Reset password" button 3rd
    * deleted the "Log in with Odoo" button
        """,
    # 'depends': ['auth_signup', 'auth_oauth', 'web', 'web_studio', 'website_sale', 'portal'],
    'depends': ['auth_signup', 'auth_oauth', 'web', 'website_sale'],
    'data': [
        "security/remove_shipping_security.xml",
        "data/data.xml",
        "views/templates.xml",
        "views/my_account_details.xml"
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
}
