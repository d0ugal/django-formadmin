from django.test import Client, TestCase


class AdminTestCase(TestCase):

    fixtures = ['users.json', ]

    def setUp(self):

        self.client = Client()
        self.client.login(username='admin', password='password')

    def test_index(self):

        r = self.client.get("/admin/")

        self.assertEqual(r.status_code, 200)

    def test_app_index(self):

        for path in ['/admin/AdminForms/', '/admin/FormAdmin/', ]:

            r = self.client.get(path)

            self.assertEqual(r.status_code, 200,
                "'%s' loaded with status code %s'" % (path, r.status_code))

    def test_form_render(self):

        for path in ['/admin/AdminForms/emailform/',
                '/admin/AdminForms/emailform/?email=test',
                '/admin/FormAdmin/uploadform/']:

            r = self.client.get(path)

            self.assertEqual(r.status_code, 200,
                "'%s' loaded with status code %s'" % (path, r.status_code))

    def test_email_form(self):

        r = self.client.post("/admin/AdminForms/emailform/", {
            'email': 'testing_email@test.com'
        }, follow=True)

        self.assertEqual(len(r.redirect_chain), 1)
        self.assertEqual(r.status_code, 200)
        last_path, last_status_code = r.redirect_chain[-1]
        self.assertTrue(last_path.endswith('/admin/'),
            "%s didn't end with /admin/AdminForms/" % last_path)

        r = self.client.post("/admin/AdminForms/emailform/", {
            'email': 'testing_email2@test.com',
            '_addanother': '1',
        }, follow=True)

        self.assertEqual(len(r.redirect_chain), 1)
        self.assertEqual(r.status_code, 200)
        last_path, last_status_code = r.redirect_chain[-1]
        self.assertTrue(last_path.endswith('/admin/AdminForms/emailform/'),
            "%s didn't end with /admin/AdminForms/emailform/" % last_path)

    def test_email_form_errors(self):

        r = self.client.post("/admin/AdminForms/emailform/", {
            'email': '?',
        }, follow=True)

        self.assertEqual(len(r.redirect_chain), 0)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Enter a valid e-mail address.")


class RegisterTestCase(TestCase):

    def test_add_form(self):

        from django import forms
        from formadmin.sites import register, AlreadyRegistered

        class MyForm(forms.Form):
            name = forms.CharField()

        register(MyForm)

        with self.assertRaises(AlreadyRegistered):
            register(MyForm)


class TestAdminHacks(TestCase):

    def test_fake_model(self):

        from django import forms
        from formadmin.hacks import create_model_like_form

        class MyForm2(forms.Form):
            field1 = forms.CharField()

        model_like_form = create_model_like_form(MyForm2)

        self.assertEqual(model_like_form._meta.verbose_name, "MyForm2")
