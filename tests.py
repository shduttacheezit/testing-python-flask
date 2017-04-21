"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("having a party", str(result.data))

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get("/", follow_redirects=True)

        self.assertIn("Please RSVP", str(result.data))
        self.assertNotIn("Party Details", str(result.data))

    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertNotIn("Please RSVP", str(result.data))
        self.assertIn("Party Details", str(result.data))

        # FIXME: check that once we log in we see party details--but not the form!
        # print "FIXME"

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info = {'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertNotIn("Party Details", str(result.data))
        self.assertIn("kind of awkward", str(result.data))


if __name__ == "__main__":
    unittest.main()
