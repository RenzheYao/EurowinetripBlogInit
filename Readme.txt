European Wine Trip Blog (www.eurowinetrip.com)
This repository contains the source code for the European Wine Trip blog, built to deliver content to audiences in Mainland China as well as international expats in Hong Kong and Mainland China.

Technical Architecture & Evolution
Frontend: Built with React to deliver a fast, interactive user interface.
Backend: Folder Eurowinetrip

Initial Development Build: Originally designed as a full-stack application where the React frontend dynamically fetched blog posts, images, and metadata directly from the Django backend database (/Eurowinetrip).

Production Build: For the live published version, the direct runtime connection between React and Django was disconnected. An export script (export.py) serializes the Django content into static .json files, allowing the React application to fetch data locally without contacting a live backend server. Backend (/Eurowinetrip): Serves as a headless CMS used exclusively for creating and managing blog content.

Note: The /Media folder (containing original blog posts and assets) is excluded from this public GitHub repository for privacy and data protection.

Key Architectural Advantages
Optimized Load Times in Mainland China: Because the site is hosted outside Mainland China, severing the live server requests and serving pre-rendered JSON client-side significantly improves page load speed across the Great Firewall (GFW).

Reduced Infrastructure Costs: Eliminates the ongoing expense of renting and maintaining a live production database/application server.

Regulatory Compliance: Removing server-side data collection simplifies compliance with local internet and data protection regulations.
