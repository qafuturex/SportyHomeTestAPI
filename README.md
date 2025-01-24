# PoetryDB API Test Cases

This document outlines the test cases implemented to verify the functionality of the PoetryDB API.

## Test Cases

| **Test Case**                         | **Steps**                                                                                                                                              |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1. Test retrieving poems by author** | 1. Send a request to `/author/{author name}/title` endpoint. <br> 2. Validate the response structure. <br> 3. Validate that each poem matches the Pydantic model. |
| **2. Test searching for a poem by title** | 1. Get a list of random poem titles. <br> 2. Select a title. <br> 3. Retrieve poem details. <br> 4. Validate the poem structure.                        |
| **3. Test retrieving author information** | 1. Get a list of authors. <br> 2. Select a random author. <br> 3. Retrieve author details. <br> 4. Validate author's poems structure
