from collections import OrderedDict

from flask_wtf import Form
from wtforms import SelectField, StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import Unique

from lib.util_wtforms import ModelForm, choices_from_dict
from snakeeyes.blueprints.user.models import db, User


class SearchForm(Form):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    # Hello. This is Nick from the future (July 2022 to be exact). I modified
    # things by adding this hidden form field to the admin users and coupons
    # pages. This hidden field is now also included in both admin index pages
    # that include the bulk delete form:
    #
    # It's on line 22 in the admin/user/index.html page and line 34 in the
    # admin/coupon/index.html page. No inline comments were added there.
    q = HiddenField('Search term', [Optional(), Length(1, 10)])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserForm(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    username = StringField(validators=[
        Unique(
            User.username,
            get_session=lambda: db.session
        ),
        Optional(),
        Length(1, 16),
        # Part of the Python 3.7.x update included updating flake8 which means
        # we need to explicitly define our regex pattern with r'xxx'.
        Regexp(r'^\w+$', message=username_message)
    ])

    role = SelectField('Privileges', [DataRequired()],
                       choices=choices_from_dict(User.ROLE,
                                                 prepend_blank=False))
    active = BooleanField('Yes, allow this user to sign in')
