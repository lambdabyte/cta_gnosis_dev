from . import List_View
from flask import render_template, redirect
from ... import db

class SQL_ORM_Add_View(List_View):
    """Add Entry to SQL DB w/ ORM Models

    Arguments:
        List_View {parent class} -- Flask class-based view
    """    
    def get_form(self):
        raise NotImplementedError

    def get_model(self):
        raise NotImplementedError

    def get_redirect(self):
        raise NotImplementedError

    def add_model_to_db(self):
        """Add entry to database
        """        
        db.session.add(self.model)
        db.session.commit()

    def dispatch_request(self):
        """Overrides parent dispatch w/ ORM add functionality

        Returns:
            template -- html template render method
        """        
        form = self.get_form()
        if form.validate_on_submit():
            # Instance of new user model
            self.model = self.get_model()
            self.add_model_to_db()
            # Redirect on successful login
            return redirect(self.get_redirect())
        # Get template contextual arguments
        context = self.get_context()
        return self.render_template(context)