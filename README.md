# DS2002 Chatbot Project

A Flask-based chatbot assistant for Discovering New Music
Ask the bot for an artist's most popular songs, and it will return their top 10 songs on Spotify.
Any other requests will be handled by GeminiAI, making the chatbot useful for a myriad of tasks.

Original Local Dataset: https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs
Cleaned using the cleanup.ipynb ETL script

Integrated with the Spotify API

How to use the bot: From the command line, type:

curl -X POST http://34.123.254.41:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"YOUR MESSAGE HERE"}'


Examples:

curl -X POST http://34.123.254.41:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"top songs by Taylor Swift"}'

Bot Returns:
  "response": "**Most-streamed songs by Taylor Swift** 1. Cruel Summer  -  Lover  2. Fortnight (feat. Post Malone)  -  THE TORTURED POETS DEPARTMENT 3. cardigan  -  folklore 4. august  -  folklore 5. Lover  -  Lover 6. Blank Space  -  1989 7. I Can Do It With a Broken Heart  -  THE TORTURED POETS DEPARTMENT  8. I Dont Wanna Live Forever (Fifty Shades Darker)  -  reputation Stadium Tour Surprise Song Playlist 9. Dont Blame Me  -  reputation 10. Anti-Hero  -  Midnights"

Gemini Response:
curl -X POST http://34.123.254.41:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"How to make chicken noodle soup?"}'
{
  "response": "This recipe makes a classic, comforting chicken noodle soup.  Feel free to adjust seasonings and vegetables to your liking.\n\n**Yields:** 6-8 servings\n**Prep time:** 20 minutes\n**Cook time:** 1.5 - 2 hours\n\n\n**Ingredients:**\n\n* 1 whole chicken (about 3-4 pounds), or 8 bone-in, skin-on chicken thighs\n* 12 cups water\n* 2 carrots, peeled and chopped\n* 2 celery stalks, chopped\n* 1 medium onion, chopped\n* 2 cloves garlic, minced\n* 1 teaspoon dried thyme\n* 1/2 teaspoon dried rosemary\n* 1/2 teaspoon salt\n* 1/4 teaspoon black pepper\n* 1 cup egg noodles (or your preferred pasta)\n* Fresh parsley, chopped (for garnish, optional)\n\n\n**Equipment:**\n* Large stockpot or Dutch oven\n\n\n**Instructions**\n\n**Get started:**\n\n1. **Prepare the chicken:** If using a whole chicken, rinse it thoroughly inside and out. If using chicken thighs, skip this step.\n\n**Make the broth:**\n\n1. **Simmer the chicken:** Place the chicken and water in the stockpot. Bring to a boil over high heat, then reduce heat to low, cover, and simmer for at least 1 hour, or until the chicken is cooked through.  If using bone-in, skin-on thighs, reduce simmer time to about 45 minutes.\n2. **Remove the chicken:** Carefully remove the chicken from the pot and set aside to cool slightly. Once cool enough to handle, shred the chicken meat, discarding the skin and bones.  (You can also use two forks to shred the chicken directly in the pot if you prefer.)\n3. **Add vegetables:** Add the carrots, celery, onion, garlic, thyme, rosemary, salt, and pepper to the broth.  Bring back to a simmer and cook for about 20 minutes, or until the vegetables are tender.\n\n**Finish the soup:**\n\n1. **Add noodles:** Add the egg noodles to the soup and cook according to package directions, usually about 8-10 minutes, or until tender.\n2. **Return chicken:** Stir in the shredded chicken.\n3. **Serve:** Ladle the soup into bowls and garnish with fresh parsley, if desired.\n\n\n**Tips and Variations:**\n\n* **For a richer broth:** Roast the chicken before simmering it in the pot. This will add more depth of flavor to the broth.\n* **Add other vegetables:** Feel free to add other vegetables like diced potatoes, green beans, or corn. Add them along with the carrots and celery.\n* **Use different noodles:**  Try different types of pasta, such as ditalini, orzo, or even broken spaghetti.\n* **Spice it up:** Add a pinch of red pepper flakes for a little heat.\n* **Make it creamy:** Stir in a splash of heavy cream or milk at the end.\n* **Make it ahead:**  This soup tastes even better the next day! Store leftovers in the refrigerator for up to 3 days.\n\n\nEnjoy your homemade chicken noodle soup!\n"
}
