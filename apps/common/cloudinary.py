import cloudinary, os
from dotenv import load_dotenv


load_dotenv()

CloudinaryConfig = cloudinary.config( 
  cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key=("CLOUDINARY_API_KEY"), 
  api_secret=("CLOUDINARY_API_SECRET") 
)