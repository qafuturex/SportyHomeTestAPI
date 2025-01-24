import pytest
import requests
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional
from hamcrest import assert_that, equal_to, greater_than
from allure import step, feature, title, story
from http import HTTPStatus


BASE_URL = "https://poetrydb.org"

# Pydantic Models for Validation
class PoemModel(BaseModel):
    title: str
    author: str
    lines: List[str]
    linecount: Optional[int] = None

@feature("PoetryDB API")
class TestPoetryDB:
    @story("Retrieve Poems by Author")
    @pytest.mark.parametrize('author', ["Emily Dickinson", "Alan Seeger"])
    def test_retrieve_poems_by_author(self, author):
        """
        Test retrieving poems by an author
        Steps:
        1. Send request to /author/{author name}/title endpoint
        2. Validate response structure
        3. Validate each poem matches Pydantic model
        """
        with step(f"Send request GET /author/{author}/title"):
            response = requests.get(f"{BASE_URL}/author/{author}/title")

        with step("Verify http status code of response"):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

        with step("Verify response is not empty"):
            titles = response.json()
            assert_that(len(titles), greater_than(0)), f"No poems found for author {author}"

        with step("Get poem for first title"):
            poem_response = requests.get(f"{BASE_URL}/title/{titles[0]['title']}")
            assert_that(poem_response.status_code, equal_to(HTTPStatus.OK))

        with step("Verify that first poem in a list has expected format"):
            poem_data = poem_response.json()[0]
            try:
                validated_poem = PoemModel(**{
                    "title": poem_data["title"],
                    "author": poem_data["author"],
                    "lines": poem_data["lines"],
                    "linecount": poem_data.get("linecount")
                })
            except ValidationError as e:
                pytest.fail(f"Poem validation failed: {e}")

    story("Search Poems by Random Title")
    def test_search_random_poem_title(self):
        """
        Test searching for a poem by a random title
        Steps:
        1. Get list of random titles
        2. Select a title
        3. Retrieve poem details
        4. Validate poem structure
        """
        with step("Get some random titles"):
            count = 5
            titles_response = requests.get(f"{BASE_URL}/random/{count}")
            assert_that(titles_response.status_code, equal_to(HTTPStatus.OK))

        with step("Select title and get poem"):
            titles = titles_response.json()
            assert_that(len(titles), equal_to(count))
            selected_title = titles[0]['title']

            poem_response = requests.get(f"{BASE_URL}/title/{selected_title}")
            assert_that(poem_response.status_code, equal_to(HTTPStatus.OK))

        with step("Verify that response body correspond to the required format"):
            poem_data = poem_response.json()[0]
            try:
                validated_poem = PoemModel(**{
                    "title": poem_data["title"],
                    "author": poem_data["author"],
                    "lines": poem_data["lines"],
                    "linecount": poem_data.get("linecount")
                })
            except ValidationError as e:
                pytest.fail(f"Poem validation failed: {e}")

    @story("Retrieve Author Information")
    @pytest.mark.parametrize("author_position_in_list", [0, -1], ids=['first author in list', 'last author in list'])
    def test_author_endpoint(self, author_position_in_list):
        """
        Test retrieving author information
        Steps:
        1. Get list of authors
        2. Select a random author
        3. Retrieve author poems
        4. Validate author's poems structure
        """
        with step("Get list of authors"):
            authors_response = requests.get(f"{BASE_URL}/author")
            assert_that(authors_response.status_code, equal_to(HTTPStatus.OK), "Failed to retrieve authors list")

        with step("Verify authors list is not empty"):
            authors = authors_response.json()
            assert_that(len(authors), greater_than(0), "Authors list is empty")

        with step("Retrieve author's poems"):
            # let's select first author for detailed validation
            selected_author = authors['authors'][author_position_in_list]
            author_response = requests.get(f"{BASE_URL}/author/{selected_author}")
            assert_that(author_response.status_code, equal_to(HTTPStatus.OK),
                        f"Failed to retrieve details for author {selected_author}")
            author_poems = author_response.json()
            assert_that(len(author_poems), greater_than(0), f"No poems found for author {selected_author}")

        with step("Validate a poem from the author"):
            sample_poem = author_poems[0]
            try:
                validated_poem = PoemModel(**{
                    "title": sample_poem["title"],
                    "author": sample_poem["author"],
                    "lines": sample_poem["lines"],
                    "linecount": sample_poem.get("linecount")
                })
            except ValidationError as e:
                pytest.fail(f"Author poem validation failed: {e}")
