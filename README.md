# Audio Annotation Tool

## Using the app

Run `docker-compose up` from the root of the repository. This may take a minute or two.

Navigate to `localhost:3000` to view the app.

![alt text](image.png)

Click on any of the files to open the detail view.

![alt text](image-1.png)

Play the audio by clicking the play button. Each segment has clickable timestamps. Annotate the segment using the buttons.

Annotating more segments will move the audio file down the list on the index view. This is done so that high priority audio files --
those with the least annotations -- have more visibility.

## System design

- The backend API runs on port 5000 using Python's FastAPI. You can view the docs at `localhost:5000/docs`
- Audio files are stored in MinIO, an S3 compatible object store. You can manually upload files at `localhost:9000`
- Data is stored in PostgreSQL
- The frontend is written in React

## Assumptions

- I have assumed that audio files will be relatively short since they need to be able to be loaded into the browser's memory using the audio API rather than being streamed. Streaming would've added another layer of complexity. Likewise, segments are assumed to not be too many and have therefore not been paginated in the API.
- I assumed it was okay to hardcode endpoint addresses and passwords to services instead of using environment variables since this is not a production level application. In the same spirit, I have not used any code formatting, linting, or unit testing.
