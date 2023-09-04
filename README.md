# Tasks
1. Create a Sanic server that serves an image on / endpoint
2. The image should be a composite of 132 images on this testing API https://api.slingacademy.com/v1/sample-data/photos resized to 32x32 thumbnails
4. You can use limit and offset arguments to control pagination on this API. While this is optional and you can fetch all 132 images at the same time, you will rank higher if you show me you understand the concept of pagination.
3. You need to fetch all of 132 images concurrently
4. If you get a fetching error you should substitue a black image tile in the composite
5. If you get a image decode error you should substitute a blue image tile int the composite
6. You should use following libraries: sanic, aiohttp, opencv2

