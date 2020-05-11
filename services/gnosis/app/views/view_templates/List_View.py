from flask.views import View
from flask import render_template

class List_View(View):
    """Base Class for rendering template w/ multiple contextual arguments

    Arguments:
        View {base class} -- base class for Flask class-based views
    """    
    def get_template_name(self):
        """Overridden in subclass

        Raises:
            NotImplementedError: if subclass missing method
        """        
        raise NotImplementedError()

    def render_template(self, context):
        """Serve html template w/ contextual arguments

        Arguments:
            context {dict} -- contextual arguments as key/vals

        Returns:
            method -- html template rendering method
        """        
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        """Used by Flask Views pkg to set class as view and execute

        Returns:
            template -- html template render method
        """        
        context = self.get_context()
        return self.render_template(context)