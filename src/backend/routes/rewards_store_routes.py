from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from backend.database.firestore import db as DB, bucket
from backend.database.family_unit import subtract_current_xp
import time

router = APIRouter(prefix="/rewards_store", tags=["Rewards Store"])

@router.get("/rewards")
async def get_rewards(email: str, profile: str):
    ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(profile).collection("INDIVIDUAL REWARD")
    doc = ref.stream()
    rewards = []
    for d in doc:
        item = d.to_dict()
        if item.get("Redeemed") is True:
            continue
        rewards.append({
            "id": d.id,
            "title": item.get("Title"),
            "cost": item.get("XP Req"),
            "level_unlock": item.get("Level Req"),
            "image": item.get("Image", "")
        })
    return rewards

@router.post("/rewards")
async def add_reward(
    email: str = Form(...),
    profile: str = Form(...),
    title: str = Form(...),
    cost: int = Form(...),
    level_unlock: int = Form(...),
    image: UploadFile = File(None),
):
    reward_id = f"{profile},{title}"
    ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(profile).collection("INDIVIDUAL REWARD").document(reward_id)
    if ref.get().exists:
        raise HTTPException(status_code=400, detail="Reward already exists")
    
    image_url = ""
    if image:
        file_bytes = await image.read()
        extension = image.filename.split(".")[-1]
        filename = f"rewards/{profile}/{int(time.time())}.{extension}"
        
        blob = bucket.blob(filename)
        blob.upload_from_string(file_bytes, content_type=image.content_type)
        blob.make_public()
        image_url = blob.public_url
    
    ref.set({
        "Author": email,
        "Recipient": profile,
        "Title": title,
        "Level Req": level_unlock,
        "XP Req": cost,
        "Image": image_url,
        "Redeemed": False,
    })
    
    return {"message": f"Reward created successfully!", "image": image_url}
    
@router.post("/claim/{reward_id}")
async def claim_reward(reward_id: str, email: str = Form(), profile: str = Form()):
    ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(profile).collection("INDIVIDUAL REWARD").document(reward_id)
    doc = ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Reward not found")

    reward = doc.to_dict()
    cost = reward["XP Req"]
    level_req = reward["Level Req"]
    
    claimed = subtract_current_xp(email, profile, cost, level_req)
    
    if not claimed:
        raise HTTPException(status_code=400, detail="Not enough XP or Level too low")
    
    ref.update({"Redeemed": True})
    
    return {
        "message": f"{reward['Title']} claimed!",
    }