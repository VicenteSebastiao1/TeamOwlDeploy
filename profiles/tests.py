from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.db.models.signals import post_save
from mixer.backend.django import mixer
from .models import Club, UserProfile, Membership, DetailedClub
from .views import club


class ClubViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = mixer.blend(User)
        self.club = mixer.blend(Club, club_owner=self.user)
        self.user_profile = UserProfile.objects.get(user=self.user)

    def test_club_view_for_anonymous_user(self):
        request = self.factory.get(f"/club/{self.club.id}")
        request.user = AnonymousUser()
        response = club(request, self.club.id)
        self.assertEqual(response.status_code, 200)

    def test_club_view_for_authenticated_user(self):
        request = self.factory.get(f"/club/{self.club.id}")
        request.user = self.user
        response = club(request, self.club.id)
        self.assertEqual(response.status_code, 200)


class ClubModelTest(TestCase):
    def test_create_club(self):
        club = mixer.blend(Club)
        self.assertTrue(isinstance(club, Club))
        self.assertEqual(str(club), club.club_name)


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)

    def test_user_profile_created_when_user_created(self):
        # Check that a UserProfile object is automatically created when a User is created
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(isinstance(user_profile, UserProfile))
        self.assertEqual(user_profile.user, self.user)

    def test_user_profile_has_clubs(self):
        club1 = mixer.blend(Club)
        club2 = mixer.blend(Club)
        self.user.userprofile.clubs_subscibed.add(club1, club2)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.clubs_subscibed.count(), 2)
        self.assertTrue(club1 in user_profile.clubs_subscibed.all())
        self.assertTrue(club2 in user_profile.clubs_subscibed.all())

    def test_user_profile_has_favorite_clubs(self):
        club1 = mixer.blend(Club)
        club2 = mixer.blend(Club)
        self.user.userprofile.favorite_clubs.add(club1, club2)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.favorite_clubs.count(), 2)
        self.assertTrue(club1 in user_profile.favorite_clubs.all())
        self.assertTrue(club2 in user_profile.favorite_clubs.all())

    def test_user_profile_has_joined_clubs(self):
        club1 = mixer.blend(Club)
        club2 = mixer.blend(Club)
        self.user.userprofile.joined_clubs.add(club1, club2)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.joined_clubs.count(), 2)
        self.assertTrue(club1 in user_profile.joined_clubs.all())
        self.assertTrue(club2 in user_profile.joined_clubs.all())

    def test_user_profile_has_owned_clubs(self):
        club1 = mixer.blend(Club)
        club2 = mixer.blend(Club)
        self.user.userprofile.owned_clubs.add(club1, club2)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.owned_clubs.count(), 2)
        self.assertTrue(club1 in user_profile.owned_clubs.all())

class MembershipModelTest(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.club = mixer.blend(Club)

    def test_create_membership(self):
        membership = mixer.blend(Membership, user_profile=self.user_profile, club=self.club)
        self.assertTrue(isinstance(membership, Membership))
        self.assertEqual(str(membership), f"{self.user_profile.user.username} is a member of {self.club.club_name}")


class DetailedClubTest(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.club = mixer.blend(Club)

    def test_get_detailed_club(self):
        club = self.club
        user_profile = self.user_profile
        mixer.blend(Membership, user_profile=user_profile, club=club)
        membership = Membership.objects.filter(club=club).order_by('created_at').first()
        if membership is None:
            join_date = None
        else:
            join_date = membership.created_at
        detailed_club = DetailedClub(club=club, join_date=join_date)
        self.assertTrue(isinstance(detailed_club, DetailedClub))
        self.assertEqual(detailed_club.club, club)
        self.assertEqual(detailed_club.join_date, Membership.objects.filter(club=club, user_profile=user_profile).first().created_at)