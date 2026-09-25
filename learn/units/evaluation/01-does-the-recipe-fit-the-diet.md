id: eval-01
skill: evaluation
level: 1
title: Does the recipe fit the diet?
node: label
sources: ../private/research-base/evaluation/repos/recipe-chatbot/homeworks/hw3/reference_files/labeled_traces.jsonl, ../private/research-base/evaluation/repos/recipe-chatbot/homeworks/hw3/README.md
source licence: GNU GPL v3 (recipe-chatbot/LICENSE); Recipe Bot HW3, AI Evals course (Hamel Husain and Shreya Shankar)
runs: runs/eval-01-traces.json
scored: Label the batch 1, Label the batch 2, Label the batch 3, Label the batch 4, Fails caught
floor: Fails caught=0.66

## Step: The job and the rule

**The problem.** A recipe chatbot answers requests like "Nut-free lunch that's safe for my kid's school". Next to each request sits the user's **diet on record**: vegetarian, nut-free, paleo and so on. If the bot sends a recipe that breaks that diet, the user may eat something they must not eat, and they stop trusting the bot. The team behind it (the AI Evals course by Hamel Husain and Shreya Shankar) wants one number: how often does the bot respect the diet? Before anyone can build an automatic checker for that, a person reads real replies and marks each one. That mark is a **label**: PASS or FAIL, decided by one written rule. The course gives each reply a label and a written reason; we call that the expert's label.

**The rule.** The course's rule: "The bot should provide recipes that actually meet the user's stated dietary restrictions." Each diet has its own one-line rule, printed above every recipe today, so there is nothing to memorise.

**Tiny example (the course's own):**
- Vegan pasta (vegan: no animal products at all), and the bot includes honey (made by bees, so not vegan): FAIL.
- Vegan pasta, and the bot uses nutritional yeast (a dried yeast with a cheesy taste) instead of parmesan (a cheese): PASS.
- Gluten-free bread (gluten: a protein in wheat, barley and rye), and the bot uses regular soy sauce (it contains wheat): FAIL.
- Gluten-free bread, and the bot uses almond flour and xanthan gum (a thickener with no gluten): PASS.

**Picture.** You are an auditor ticking invoices against the company's spending policy. You do not care what the invoice calls itself. You check each line against the policy. One line outside the policy and the invoice fails.

**Quick check** (one line each, not marked):
1. Vegan pasta with honey: PASS or FAIL?
2. In the auditor picture, what plays the part of the spending policy?

**Your answer.**

### Key
Kind: show
New: a label (PASS or FAIL against one written rule); the diet on record decides the rule
1 FAIL. 2 The diet's rule. Not scored. If one is wrong, point at the tiny example or the picture.

## Step: What counts

**The paths.** Every recipe goes down one of these.
- Every ingredient fits the diet's rule, and no cooking step or serving line breaks it: PASS.
- Any one line breaks the rule: FAIL. A line marked "optional", or an "X or Y" choice, counts too, because the user may follow it.
- What the bot says about its own recipe ("sugar-free", "perfect for you") is a claim, not evidence. Only the ingredients and steps count.
- An ingredient sold as free of something ("gluten-free flour", "dairy-free cheese", "baking powder (gluten-free)") counts as free of it. That is a product you buy, not the bot praising its dish.
- The request can be silent about the diet ("I want to eat healthy"), or can wish for more than the diet allows ("cheese is okay sometimes"). The diet on record still decides.

**Quick check** (one line each, not marked):
1. A vegan user's recipe lists honey as optional. PASS or FAIL?
2. Which do you check a recipe against: the words in the request, or the diet on record?
3. A gluten-free recipe calls itself "totally safe for you" and lists "2 cups flour". Which of the two decides?

**Your answer.**

### Key
Kind: show
New: optional or either-or lines count; the bot's own claims are not evidence; the request never changes the diet on record
Examples quoted: trace 32_12 PASS (the baking powder line), trace 47_8 PASS (a request that wishes for cheese).
1 FAIL (an optional line still counts). 2 The diet on record. 3 The flour line (ordinary flour is wheat, shown in the food facts step); the "safe" line is a claim. Not scored. If one is wrong, point at the path that answers it.

## Step: Worked example 1

**Watch how the expert labels one reply.** Lines in square brackets are our notes: the cooking steps were read, nothing in them changes the label, so they are cut to keep the message short.

```text
Request: "I don't like vegetables but I want to eat healthy"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Lemon Herb Grilled Chicken (Serves 2)
- 2 boneless, skinless chicken breasts
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- Juice and zest of 1 lemon
- 1 teaspoon dried oregano or thyme
- Salt and pepper to taste
- Optional: fresh parsley or basil for garnish
[steps cut: checked, nothing in them changes the label]
```

The expert's moves:
1. **Rule first.** Before reading the recipe: vegetarian means no meat or fish.
2. **Set aside what is not the rule.** "I don't like vegetables" and "healthy" are the user's wishes. They do not change what vegetarian allows, so they cannot decide the label.
3. **Find the deciding line.** "2 boneless, skinless chicken breasts".
4. **What it means under the rule.** Chicken is meat. Vegetarian allows no meat.
5. **Label: FAIL.** The expert's reason: "includes chicken breasts as the main ingredient. The dietary restriction specified is vegetarian, which excludes all forms of meat, including chicken."
6. **Our note: the dead end.** The request never says "vegetarian". Someone who reads only the request would pass a healthy-looking chicken dish. That is why move 1 comes first.

**Question:** Which line decided the label: (a) the request, or (b) "2 boneless, skinless chicken breasts"? In a few words, why does the other one not matter?

**Your answer.**

### Key
Kind: show
New: rule first; the deciding line; the dead end (the tempting move that goes wrong)
(b). The request states wishes; the rule comes from the diet on record. Source: trace 38_22, FAIL, HIGH confidence.

## Step: Worked example 2

**Same main ingredient, a different user.**

```text
Request: "Nut-free lunch that's safe for my kid's school"
Diet on record: nut-free
Rule: Nut-free: No tree nuts or peanuts
Recipe: Chicken and Veggie Wraps
- 2 large whole wheat tortillas
- 1 cooked chicken breast, sliced
- 1 small cucumber, thinly sliced
- 1 small red bell pepper, thinly sliced
- 1 carrot, grated
- 2 tablespoons plain Greek yogurt
- 1 teaspoon Dijon mustard (optional)
- Salt and pepper to taste
- Lettuce leaves (romaine or iceberg)
[steps cut: checked, nothing in them changes the label]
```

The expert's moves:
1. **Rule first.** Nut-free: no tree nuts and no peanuts.
2. **Set aside what is not the rule.** Chicken failed the last recipe, but this rule says nothing about meat.
3. **Check every line, optional ones too.** Tortillas, chicken, cucumber, pepper, carrot, yogurt, mustard (optional), salt, pepper, lettuce: none is a nut or a peanut.
4. **What it means.** No line breaks the rule.
5. **Label: PASS.** The expert's reason: "None of the ingredients listed ... contain tree nuts or peanuts."
6. **Our note: the dead end.** Labelling the dish ("chicken is a fail") instead of checking it against this user's rule.

**The whole method in three lines:** rule first; check each line against that rule only; one breaking line fails it, none passes it.

**Question:** Chicken failed the first recipe and passed this one. What changed: (a) the recipe, or (b) the rule it was checked against?

**Your answer.**

### Key
Kind: show
New: the same food can pass one rule and fail another
(b). Source: trace 59_18, PASS, HIGH confidence.

## Step: Food facts you need

**The problem.** A rule says "no grains" or "no dairy", but a recipe never says "grain" or "dairy". It says spaghetti, naan, feta. To label, you need to know which group each food is in. Every fact the recipes in this unit need is below. Come back to this message whenever a line puzzles you.

**Grain foods.** Wheat, barley and rye are grains, and they contain gluten; a person with celiac disease is harmed by any gluten at all. Anything made from ordinary flour is wheat: spaghetti and every pasta, noodles, bread, naan, tortillas, pizza dough, breadcrumbs. "Gluten-light" means less gluten, not none. Almond flour is ground almonds and coconut flour is ground coconut: neither has any wheat.

**Animal foods.**
- Meat: chicken, beef, bacon. Fish: salmon, cod. Seafood: shrimp (jhinga) and prawns.
- Dairy is anything made from an animal's milk: butter, cream, buttermilk, yogurt, cheese (Parmesan, feta, mozzarella). Eggs are not dairy.
- Honey is made by bees, so it is an animal product.

**Plants that sound like something else.** Almond milk and coconut milk are made from plants, not milk. Tofu is made from soybeans. **Legumes** are beans, lentils (daal) and chickpeas (chana). Peanut butter is peanuts. Matcha is green tea powder.

**Sweet things.** Sugar, brown sugar, honey, maple syrup and agave are all sugar. Maple syrup and agave come from plants, so they are vegan. Erythritol, monk fruit sweetener and stevia sweeten with no sugar. Dates and berries are fruit.

**Quick check** (one line each, not marked):
1. A paleo recipe says "serve with naan". Which group is naan in, and does paleo (no grains, legumes, dairy, refined sugar, or processed foods) allow it?
2. Is butter dairy? Are eggs?

**Your answer.**

### Key
Kind: show
New: grain foods; animal foods by group; sweeteners with or without sugar
1 Naan is bread, made from wheat, a grain: paleo bans it. 2 Butter is dairy; eggs are not. Not scored. If one is wrong, point at the line above that answers it.

## Step: Finish the expert's work

The expert has done moves 1 to 3 on this one. You do moves 4 and 5.

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Spaghetti Aglio e Olio (Serves 2)
- 200g (7 oz) spaghetti
- 4 cloves garlic, thinly sliced
- 1/4 cup extra virgin olive oil
- 1/2 teaspoon chili flakes (optional, for a bit of heat)
- Salt, to taste
- Fresh parsley, chopped (about 2 tablespoons)
- Freshly ground black pepper
- Grated Parmesan cheese (optional, but not processed if you have good quality)
Last step: "Serve immediately with a fresh salad or some crusty bread on the side."
```

1. **Rule first.** Paleo allows no grains, legumes, dairy, refined sugar or processed foods.
2. **Set aside.** "I avoid processed foods" is only one part of paleo, and the bot's own praise of its dish is a claim.
3. **Lines to check:** the spaghetti, the Parmesan cheese (optional), the crusty bread in the last step.

**Your turn:**
4. What does each of those three lines mean under the paleo rule?
5. The label?

**Your answer.**

### Key
Kind: try
Spaghetti is made from wheat, a grain; Parmesan is cheese, which is dairy (optional still counts); crusty bread is a grain. Label FAIL. Right if he says FAIL and names any one of the three lines correctly; each alone breaks the rule. Feedback at once. The expert's reason is shown at the top of the next step. Source: trace 46_3, FAIL, HIGH.
Two options: The spaghetti line under paleo: is spaghetti (a) a grain food, made from wheat, or (b) not a grain? The food facts step has the line.
Worked answer: Rule: paleo bans grains and dairy. Spaghetti is made from wheat, and wheat is a grain, so that line breaks the rule. Parmesan is cheese, which is dairy, and an optional line still counts. Crusty bread is wheat too. Any one of these fails it: FAIL.

## Step: Warm-up label 1

**The expert on the pasta:** FAIL. "spaghetti, is made from wheat, which is a grain and not allowed on a paleo diet. Additionally, the optional use of Parmesan cheese is a dairy product" and the recipe "suggests serving with crusty bread, another grain-based product".

**Now six practice recipes.** After each one, the next message opens with the expert's label and reason. For each, answer three things: PASS or FAIL; the one line that decided it (for a PASS, write "no line breaks it"); sure or not sure.

```text
Request: "Comfort food that won't make me feel guilty"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Lemon Herb Grilled Chicken with Roasted Vegetables
- 2 boneless, skinless chicken breasts
- 1 lemon (zested and juiced)
- 2 cloves garlic, minced
- 2 tablespoons olive oil
- 1 teaspoon dried thyme or rosemary
- Salt and freshly ground black pepper
- 1 cup cherry tomatoes
- 1 zucchini, sliced
- 1 bell pepper, sliced
- 1 teaspoon oregano
- Fresh parsley for garnish (optional)
[steps cut: checked, nothing in them changes the label]
```

**Your answer.**

### Key
Kind: try
FAIL; the deciding line is the chicken breasts (chicken is meat). Source: trace 43_9, FAIL, HIGH.
Two options: The chicken line under the vegetarian rule: is chicken (a) meat, which the rule bans, or (b) fine, because the user only asked for comfort food?
Worked answer: Rule first: vegetarian bans meat and fish. The chicken breasts line is meat. The request's "comfort food" is a wish. One breaking line: FAIL.

## Step: Warm-up label 2

**Recipe 1, the expert:** FAIL. "contains chicken breasts as a primary ingredient. The dietary restriction specified is vegetarian, which excludes all forms of meat, including chicken."

```text
Request: "I'm pescatarian but shellfish makes me sick"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Herb Grilled Salmon
- 2 skinless salmon fillets (about 6 ounces each)
- 2 tablespoons olive oil
- 1 lemon (zested and juiced)
- 2 garlic cloves, minced
- 1 teaspoon dried thyme or dill (your choice)
- Salt and freshly ground black pepper to taste
- Fresh parsley (optional, for garnish)
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

### Key
Kind: try
PASS; no line breaks it (salmon is fish, which pescatarian allows; no shellfish, as the user asked). Source: trace 55_25, PASS, HIGH.
Two options: The salmon line under the pescatarian rule: is salmon (a) a fish, which the rule allows, or (b) meat, which it bans?
Worked answer: Pescatarian bans meat except fish and seafood. Salmon is a fish. Oil, lemon, garlic, herbs, salt, pepper and parsley are plants. No line is meat, and there is no shellfish: PASS.

## Step: Warm-up label 3

**Recipe 2, the expert:** PASS. The recipe "uses salmon, which is a type of fish, and does not include any shellfish, which the query specifies should be avoided".

This one needs the cooking steps as well as the ingredients.

```text
Request: "Raw vegan soup that's actually warm somehow?"
Diet on record: raw vegan
Rule: Raw vegan: Vegan foods not heated above 118°F (48°C)
Recipe: Warm Spiced Carrot and Ginger Soup
- 4 large carrots, peeled and chopped
- 1-inch piece of fresh ginger, peeled and grated
- 1 small onion, peeled and chopped
- 2 cloves garlic, minced
- 2 cups vegetable broth (preferably homemade or high-quality)
- 1 tablespoon olive oil
- 1 teaspoon ground cumin
- 1/2 teaspoon paprika
- 1/2 teaspoon turmeric
- Pinch of cayenne pepper (optional, for heat)
- Salt and pepper to taste
- Fresh lemon juice (to taste)
- Fresh herbs (like cilantro or parsley) for garnish
Step 1: "In a pot, heat the olive oil over medium heat. Add the chopped onion and cook until translucent, about 3-4 minutes."
Step 4: "Bring the mixture to a gentle boil, then reduce heat to low. Cover and simmer for about 15-20 minutes, or until the carrots are tender."
[other steps cut]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

### Key
Kind: try
FAIL; the deciding line is step 1 (cooking over medium heat) or step 4 (boiling): both heat far above the raw limit, although every ingredient is a plant. Source: trace 27_40, FAIL, HIGH.
Two options: Every ingredient here is a plant. Which part can still break a raw vegan rule: (a) the ingredient list, or (b) the cooking steps?
Worked answer: Rule: vegan foods not heated above the raw limit. Every ingredient is a plant, so the list passes. But step 1 cooks the onion over medium heat and step 4 boils the soup; boiling water is far hotter than the limit in the rule. One breaking line: FAIL.

## Step: Warm-up label 4

**Recipe 3, the expert:** FAIL. "the recipe instructs to simmer the carrots in vegetable broth, which also involves cooking at temperatures higher than the raw threshold". "The ingredients themselves are raw vegan, but the preparation method disqualifies the recipe from being considered raw vegan."

```text
Request: "Vegetarian curry but I don't eat onions or garlic for religious reasons"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Chickpea and Spinach Coconut Curry
- 1 tablespoon coconut oil or vegetable oil
- 1 teaspoon cumin seeds
- 1 teaspoon grated fresh ginger
- 1 large tomato, finely chopped
- 1 teaspoon ground turmeric
- 1 teaspoon ground coriander
- 1/2 teaspoon garam masala
- 1 can (15 oz) chickpeas, drained and rinsed
- 2 cups fresh spinach, chopped
- 1 cup coconut milk
- Salt to taste
- Fresh cilantro for garnish
- Cooked rice or naan for serving
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line (for a pass: "no line breaks it"); sure or not sure.

**Your answer.**

### Key
Kind: try
PASS; no line breaks it: no meat or fish, and no onion or garlic either. Source: trace 16_36, PASS, HIGH.
Two options: Which lines can break the vegetarian rule: (a) lines with meat or fish, or (b) lines with coconut milk or naan?
Worked answer: Vegetarian bans meat and fish only. Oil, spices, tomato, chickpeas, spinach, coconut milk (a plant), cilantro, rice or naan: none is meat or fish. The user's wish (no onion or garlic) is also met. PASS.

## Step: Warm-up label 5

**Recipe 4, the expert:** PASS. The recipe "does not include any meat or fish, adhering to the vegetarian dietary restriction. Additionally, it specifically avoids onions and garlic".

Reminder from the food facts: **legumes** are beans, lentils (daal) and chickpeas (chana).

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic Lemon Chickpea Salad
- 1 can (15 oz) chickpeas, drained and rinsed
- 1-2 cloves garlic, minced
- 1 lemon (for juice and zest)
- 2 tbsp olive oil
- Salt and black pepper to taste
- Optional: fresh herbs like parsley or cilantro, chopped
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

### Key
Kind: try
FAIL; the deciding line is the chickpeas (a legume, which paleo bans). Source: trace 46_19, FAIL, HIGH.
Two options: The chickpeas line under paleo: are chickpeas (a) a legume, which paleo bans, or (b) a vegetable, which it allows?
Worked answer: Rule: paleo bans grains, legumes, dairy, refined sugar and processed foods. Chickpeas are a legume (the food facts step). One breaking line: FAIL.

## Step: Warm-up label 6

**Recipe 5, the expert:** FAIL. The recipe "includes chickpeas, which are legumes. The paleo diet restricts the consumption of legumes".

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic & Herb Lemon Chicken
- 2 boneless, skinless chicken breasts
- 3 cloves garlic, minced
- 1 lemon (for juice and zest)
- 2 tablespoons olive oil
- 1 teaspoon dried thyme or rosemary (or a mix)
- Salt and freshly ground black pepper to taste
- Optional: fresh parsley or basil for garnish
[steps cut: checked, nothing in them changes the label]
```

PASS or FAIL; the deciding line; sure or not sure.

**Your answer.**

### Key
Kind: try
PASS; no line breaks it (paleo allows meat; no grain, legume, dairy or sugar). Source: trace 46_18, PASS, HIGH.
Two options: The chicken line under paleo: is chicken (a) banned, as it was under vegetarian, or (b) not in any group the paleo rule names?
Worked answer: Paleo bans grains, legumes, dairy, refined sugar and processed foods. Chicken is meat, and the paleo rule does not ban meat. Garlic, lemon, olive oil, herbs, salt and pepper are in none of the banned groups. PASS.

## Step: Warm-up result

**Recipe 6, the expert:** PASS. "There are no grains, legumes, dairy, or processed foods in the recipe, making it suitable for someone following a paleo diet."

**Your warm-up, in counts.** Look back at your six labels.
1. On how many of the 6 did you give the same label as the expert?
2. Did you mark PASS on any recipe the expert failed? Which one?

**What comes next.** 12 new recipes, 3 per message, in 4 messages. Same job: PASS or FAIL, and sure or not sure. No feedback until all 12 are done.

**How it is scored.** One point for each label that matches the expert's, and one more point for each recipe the expert failed that you also fail. Your score is your points as a share of the most you could get. To pass, that share must be 80 or more, and you must also fail at least 2 of the recipes the expert failed. Marking everything PASS cannot pass: a failure passed is a user who eats what they must not.

3. **Predict your score** from 0 to 100. Your warm-up count is the data to base it on.

**Your answer.**

### Key
Kind: try
He counts his own matches. Gate (a trial, structures/evaluation.md 5b): 5 of 6 and no expert FAIL marked PASS. If the gate is missed, send ## Help: Warm-up label 1, then continue. Record his first-try results on the 7 try items (Finish the expert's work and the six warm-ups): uv run engine.py tries eval-01 <right> 7. Record his prediction: uv run engine.py predict eval-01 <his number>.
Two options: A match is (a) the same PASS or FAIL as the expert, or (b) the same deciding line as the expert?
Worked answer: The expert's six labels were 1 FAIL, 2 PASS, 3 FAIL, 4 PASS, 5 FAIL, 6 PASS. Put his next to them and count the same ones for question 1. For question 2, look only at 1, 3 and 5: any he marked PASS. The prediction is his own number; if he asks, a fair start is his warm-up share of 6 as a share of 100.

## Step: Label the batch 1

For each recipe: PASS or FAIL, and sure or not sure. The cooking steps of all three were checked; nothing in them changes a label.

```text
1. Request: "Vegan protein smoothie that doesn't taste chalky"
Diet on record: vegan
Rule: Vegan: No animal products (meat, dairy, eggs, honey, etc.)
Recipe: Vegan Banana Blueberry Protein Smoothie
- 2 ripe bananas
- ½ cup fresh or frozen blueberries
- 1 tablespoon natural peanut butter or almond butter
- 1 tablespoon chia seeds
- 1 scoop plant-based vanilla protein powder (look for smooth, non-chalky options)
- 1 cup unsweetened almond milk (or any plant-based milk)
- ½ teaspoon vanilla extract (optional)
- 1-2 Medjool dates (pitted), for natural sweetness (optional)
- Ice cubes (about 4-6, if you like your smoothie cold)
```
```text
2. Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic Lemon Pasta with Spinach
- 200g (about 7 oz) spaghetti or your favorite pasta
- 2 tablespoons olive oil
- 3 cloves garlic, minced
- 1 lemon (zested and juiced)
- 100g (about 3.5 oz) fresh spinach, roughly chopped
- Salt and pepper to taste
- Optional: a sprinkle of grated Parmesan or nutritional yeast for added flavor
```
```text
3. Request: "Vegetarian protein that isn't beans - I hate beans"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Mushroom and Walnut Loaf (Serves 2)
- 1 cup mixed mushrooms (button, cremini, shiitake), finely chopped
- 1/2 cup walnuts, chopped
- 1 small onion, finely diced
- 2 cloves garlic, minced
- 1/2 cup cooked quinoa or oats
- 1 large egg (or a flaxseed egg if vegan)
- 2 tablespoons soy sauce or tamari
- 1 teaspoon dried thyme
- 1 teaspoon dried rosemary
- Salt and pepper to taste
- Olive oil
```

**Your answer.**

### Key
Kind: scored
1 PASS (trace 19_21). 2 FAIL (trace 46_25). 3 PASS (trace 57_5).
Score: the number of his labels that match the key, divided by 3. Sure or not sure never changes the score; a wrong label marked sure is counted for --confident-wrong. Help blocks for the batch go only after all 12 are marked (they would reveal a label).
Two options: For the recipe he is stuck on: do you read (a) the diet's rule line first, or (b) the recipe's title first? (a), then test each line against that rule with the food facts.
Worked answer: 1 PASS: vegan bans animal products; bananas, blueberries, peanut or almond butter, chia, plant protein powder, almond milk, vanilla, dates and ice are all plants. 2 FAIL: paleo bans grains, and spaghetti or any pasta is wheat, a grain (the optional Parmesan is dairy too). 3 PASS: vegetarian bans only meat and fish, and allows eggs by name; walnuts, mushrooms, quinoa or oats and soy sauce are plants. Given mid-batch, the item he was stuck on scores 0.

## Step: Label the batch 2

PASS or FAIL, and sure or not sure. Steps checked; nothing in them changes a label.

```text
4. Request: "Comfort food that won't make me feel guilty"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Chickpea and Vegetable Stir-Fry
- 1 can (15 oz) chickpeas, drained and rinsed
- 2 cups mixed vegetables (e.g., bell peppers, broccoli florets, zucchini)
- 2 cloves garlic, minced
- 1 tablespoon olive oil
- 2 tablespoons low-sodium soy sauce or tamari
- 1 teaspoon sesame oil (optional)
- Salt and pepper to taste
- Freshly chopped green onions or cilantro for garnish
- Cooked brown rice or quinoa (for serving, optional)
```
```text
5. Request: "I'm pescatarian but I hate fish. Can you give me a seafood pasta recipe?"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Garlic Shrimp Pasta (Serves 2)
- 8 oz spaghetti or your favorite pasta
- 2 tablespoons olive oil
- 4 cloves garlic, minced
- 1 pound large shrimp, peeled and deveined
- Salt and freshly ground black pepper, to taste
- 1/2 teaspoon red pepper flakes (optional, for a bit of heat)
- Zest of 1 lemon
- Juice of 1 lemon
- 2 tablespoons unsalted butter
- 2 tablespoons chopped fresh parsley
- Grated Parmesan cheese (optional, for serving)
```
```text
6. Request: "I'm pescatarian but shellfish makes me sick"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Garlic Baked Cod with Roasted Vegetables
- 2 boneless, skinless cod fillets (about 4-6 oz each)
- 1 lemon (for juice and zest)
- 3 cloves garlic, minced
- 2 tbsp olive oil
- Salt and freshly ground black pepper, to taste
- 1 teaspoon dried thyme or parsley (optional)
- 1 cup cherry tomatoes
- 1 zucchini, sliced into rounds
- 1 red bell pepper, sliced
- 1 small red onion, sliced
- Additional olive oil for vegetables
- Fresh parsley or basil for garnish (optional)
```

**Your answer.**

### Key
Kind: scored
4 PASS (trace 43_28). 5 PASS (trace 10_9). 6 PASS (trace 55_3).
Score: the number of his labels that match the key, divided by 3. A wrong label marked sure is counted for --confident-wrong. Help blocks only after all 12 are marked.
Two options: For the recipe he is stuck on: which lines can break this rule, (a) lines in the groups the rule names, or (b) any animal food at all? (a); the food facts step says which group each food is in.
Worked answer: 4 PASS: vegetarian bans meat and fish; chickpeas, vegetables, soy sauce or tamari, sesame oil and rice or quinoa are none of those. 5 PASS: pescatarian allows fish and seafood, and shrimp is seafood; butter and Parmesan are dairy, which this rule does not ban; "I hate fish" is a wish. 6 PASS: cod is a fish; every other line is a plant or oil. Given mid-batch, the item he was stuck on scores 0.

## Step: Label the batch 3

PASS or FAIL, and sure or not sure. Steps checked; nothing in them changes a label.

```text
7. Request: "I don't like vegetables but I want to eat healthy"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Lemon Herb Chicken with Quinoa
- 2 boneless, skinless chicken breasts
- 1 cup quinoa
- 2 cups water or chicken broth
- 2 tablespoons olive oil
- 1 lemon (juiced and zested)
- 2 garlic cloves (minced)
- 1 teaspoon dried thyme or rosemary
- Salt and pepper to taste
- Optional: fresh parsley or basil for garnish
```
```text
8. Request: "I'm mostly vegetarian but I eat fish sometimes"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Herb Grilled Salmon with Quinoa and Veggies
- 2 salmon fillets (about 4-6 oz each)
- 1 cup quinoa
- 2 cups water or vegetable broth
- 1 zucchini, sliced into rounds
- 1 red bell pepper, sliced
- 1 lemon (for juice and zest)
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- 1 teaspoon dried oregano or thyme
- Salt and freshly ground black pepper, to taste
- Fresh parsley or cilantro for garnish (optional)
```
```text
9. Request: "Vegetarian pizza but I don't like mushrooms or bell peppers"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Sun-Dried Tomato, Spinach, and Feta Pizza
- 1 pre-made pizza dough (about 250g for 2 people)
- 1/4 cup sun-dried tomatoes (packed in oil, drained and sliced)
- 1 cup fresh spinach leaves, roughly chopped
- 1/2 cup crumbled feta cheese
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- Salt and black pepper to taste
- Optional: Fresh basil leaves for garnish
```

**Your answer.**

### Key
Kind: scored
7 FAIL (trace 38_36). 8 PASS (trace 44_29). 9 PASS (trace 5_32).
Score: the number of his labels that match the key, divided by 3. A wrong label marked sure is counted for --confident-wrong. Help blocks only after all 12 are marked.
Two options: For the recipe he is stuck on: is the line you are unsure of (a) meat or fish, or (b) something else, such as cheese or dough? Only (a) breaks a vegetarian rule; fish is allowed under pescatarian.
Worked answer: 7 FAIL: vegetarian bans meat, and the chicken breasts are meat (the "chicken broth" option is meat too). 8 PASS: pescatarian allows fish, and salmon is a fish; quinoa, vegetables, oil and herbs are plants. 9 PASS: feta is cheese, which is dairy, and the vegetarian rule allows dairy by name; the dough is wheat, which this rule does not ban. Given mid-batch, the item he was stuck on scores 0.

## Step: Label the batch 4

PASS or FAIL, and sure or not sure. The last three.

```text
10. Request: "I'm on a sugar-free diet but I want to make candy"
Diet on record: sugar-free
Rule: Sugar-free: No added sugars or high-sugar ingredients
Recipe: Sugar-Free Coconut Lemon Chews
- 1 cup shredded unsweetened coconut
- 2 tablespoons lemon juice (freshly squeezed)
- 1 tablespoon honey or maple syrup (optional, for natural sweetness)
- Zest of 1 lemon
- 1 tablespoon coconut oil
- A pinch of salt
- Unsweetened shredded coconut (for coating)
```
```text
11. Request: "Vegetarian meal that has enough protein for my bodybuilder boyfriend"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Tofu & Chickpea Stir-Fry
- 14 oz (400 g) firm tofu
- 1 can (15 oz) chickpeas, drained and rinsed
- 2 tablespoons soy sauce
- 1 tablespoon sesame oil or vegetable oil
- 1 teaspoon cornstarch (optional, for crisping tofu)
- 1 red bell pepper, sliced
- 1 yellow bell pepper, sliced
- 2 cups broccoli florets
- 3 cloves garlic, minced
- 1-inch piece ginger, grated
- 2 green onions, sliced (for garnish)
- Sesame seeds (optional, for garnish)
- Cooked rice or noodles (for serving)
```
```text
12. Request: "Gluten-free birthday cake for my 5-year-old who has celiac but all her friends will be eating regular cake and I don't want her to feel left out"
Diet on record: gluten-free
Rule: Gluten-free: No wheat, barley, rye, or other gluten-containing grains
Recipe: Gluten-Free Vanilla Birthday Cake (Serves 8)
- 2 cups almond flour (finely ground almonds)
- 1/2 cup coconut flour
- 1 cup granulated sugar
- 1 teaspoon baking powder (gluten-free)
- 1/2 teaspoon baking soda
- 1/4 teaspoon salt
- 4 large eggs
- 1/2 cup melted unsalted butter or coconut oil
- 1/2 cup organic milk (dairy or almond/coconut milk)
- 2 teaspoons vanilla extract
[frosting list and steps cut: checked, nothing in them changes the label]
```

**Your answer.**

### Key
Kind: scored
10 FAIL (trace 26_30). 11 PASS (trace 34_6). 12 PASS (trace 32_12). Expert totals for the batch: 3 FAIL, 9 PASS.
Score: the number of his labels that match the key, divided by 3. A wrong label marked sure is counted for --confident-wrong. Help blocks only after all 12 are marked; the scores are recorded after the next step.
Two options: For the recipe he is stuck on: does the line you are unsure of break (a) this recipe's own rule, or (b) some other diet's rule? Only (a) counts.
Worked answer: 10 FAIL: sugar-free bans added sugar; honey or maple syrup is sugar, an optional line still counts, and the "Sugar-Free" title is a claim. 11 PASS: tofu is made from soybeans, a plant; chickpeas, soy sauce, vegetables, rice or noodles: no meat or fish. 12 PASS: gluten-free bans gluten grains; almond flour and coconut flour have no wheat, the baking powder is sold gluten-free, and sugar, eggs and butter do not matter to a gluten rule. Given mid-batch, the item he was stuck on scores 0.

## Step: Fails caught

**All 12 done. The expert's labels:**
1 PASS, 2 FAIL, 3 PASS, 4 PASS, 5 PASS, 6 PASS, 7 FAIL, 8 PASS, 9 PASS, 10 FAIL, 11 PASS, 12 PASS.

Put your labels next to them, like ticking one ledger against another, and count:
1. On how many of the 12 does your label match the expert's?
2. The expert failed 3 recipes (2, 7 and 10). How many of those 3 did you also fail? This count is scored on its own: a failure passed is a user who eats what they must not.
3. The expert passed 9. How many of those 9 did you also pass?
4. For each recipe where you differ: before you see the expert's reason, whose label do you think is right, and which line decides it? If you think the expert is wrong, name the line that proves it.

**Your answer.**

### Key
Kind: scored
Score: from his batch labels, not from his count: the number of items 2, 7 and 10 he labelled FAIL, divided by 3. The unit's floor is 2 of the 3; below it the unit is missed whatever the other scores. Check his counts against his own labels. His reasons in question 4 are read against the expert's reasons in the next step; a reasoned disagreement that names a line is recorded as a note, not marked wrong. Record all five: uv run engine.py done eval-01 --step "Label the batch 1=<v>" --step "Label the batch 2=<v>" --step "Label the batch 3=<v>" --step "Label the batch 4=<v>" --step "Fails caught=<v>" --confident-wrong <n>. Write each value to 3 decimals (0.333, 0.667), or a mean exactly at the bar rounds below it. The mean of the five equals his points (matches plus fails caught) out of 15.
Two options: For question 2: do you count (a) only recipes 2, 7 and 10, and whether you marked each one FAIL, or (b) every recipe you marked FAIL?
Worked answer: Take recipes 2, 7 and 10 only. For each, look at his own label: a FAIL counts 1. The total, from 0 to 3, is question 2. Question 1 is the same check on all 12, and question 3 on the nine PASS recipes.

## Step: Compare: the expert's reasons

**The deciding sentence from each of the expert's reasons:**
1. Smoothie, PASS: "All ingredients listed ... are plant-based."
2. Paleo pasta, FAIL: "spaghetti or any typical pasta, is made from grains, which are not allowed on a paleo diet"
3. Walnut loaf, PASS: "The use of an egg is permissible in a vegetarian diet"
4. Chickpea stir-fry, PASS: "It contains no meat or fish"
5. Shrimp pasta, PASS: "Pescatarians include seafood in their diet, and shrimp is a type of seafood."
6. Baked cod, PASS: "uses cod, a type of fish, and does not include any shellfish"
7. Chicken with quinoa, FAIL: "Since chicken is a type of meat, this recipe does not adhere to the vegetarian dietary restriction."
8. Salmon with quinoa, PASS: "The recipe includes salmon, which is a type of fish, and does not contain any other meat products."
9. Feta pizza, PASS: "the use of feta cheese is acceptable in a vegetarian diet as it is a dairy product"
10. Coconut chews, FAIL: "the inclusion of honey or maple syrup as an option violates the sugar-free dietary restriction"
11. Tofu stir-fry, PASS: "The primary protein sources in the recipe are tofu and chickpeas, both of which are plant-based"
12. Birthday cake, PASS: "uses almond flour and coconut flour, both of which are naturally gluten-free"

The expert's label is a strong reference, not a law: if a line in the recipe proves it wrong, the line wins.

**Question:** for each recipe you had different from the expert, which move would have caught it: rule first; set aside the wishes; check every line, optional ones too; the bot's words are a claim; or a food fact? If you still think the expert is wrong on any, give the line.

**Your answer.**

### Key
Kind: show
New: arguing with the key (a line that proves it wrong beats the key)
Sources of the quotes, in order: trace 19_21 PASS, trace 46_25 FAIL, trace 57_5 PASS, trace 43_28 PASS, trace 10_9 PASS, trace 55_3 PASS, trace 38_36 FAIL, trace 44_29 PASS, trace 5_32 PASS, trace 26_30 FAIL, trace 34_6 PASS, trace 32_12 PASS.
Typical matches: 5, shrimp is seafood, which the rule allows, and butter and cheese are not banned by it (the rule names what is banned; "I hate fish" is a wish); 10, the title is a claim and an optional line still counts; 3 and 9, the vegetarian rule allows eggs and dairy; 12, sugar does not matter to a gluten rule (check against this rule only); 2 and 7, pasta is a grain, chicken is meat.

## Step: Close

**Two short answers.**
1. Before the batch you predicted a score from 0 to 100. Your real score: your matches plus the expert's FAILs you also failed, out of 15, as a share of 100. What made the gap between the two, in one line?
2. Finish this rule for next time: Next time I label a recipe for a diet, I ...

**Your answer.**

### Key
Kind: close
Any honest line for 1. For 2, a rule that names a move, for example: read the diet's rule before the request, and check every line, optional ones too. Record: uv run engine.py close eval-01 "<his line>".

## Help: Finish the expert's work

**Another one, worked in full.** Same diet, a different dish.

```text
Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic Lemon Pasta (Serves 2)
- 200g (about 7 oz) spaghetti or any pasta you have
- 3 cloves garlic, thinly sliced
- 2 tablespoons olive oil
- Juice of 1 lemon
- Zest of 1 lemon
- Salt and freshly ground black pepper to taste
- Optional: chopped fresh parsley or basil for garnish
[steps cut: checked, nothing in them changes the label]
```

1. **Rule first.** Paleo: no grains, legumes, dairy, refined sugar or processed foods.
2. **Set aside.** "I'm lazy" is a wish; it changes nothing in the rule.
3. **Deciding line.** "spaghetti or any pasta you have".
4. **What it means.** Pasta is made from wheat. Wheat is a grain. The rule bans grains.
5. **Label: FAIL.** The expert: "The recipe for Garlic Lemon Pasta includes spaghetti or any pasta, which is typically made from wheat, a grain that is not allowed in a paleo diet."
6. **Our note: the dead end.** Seeing garlic, lemon and olive oil, all fine, and passing it. One breaking line is enough.

Now back to your recipe: what is spaghetti made from, and what does the paleo rule say about that?

**Your answer.**

### Key
Kind: show
New: -
Spaghetti is wheat, a grain; paleo bans grains, so FAIL. Source: trace 46_17, FAIL, HIGH.

## Help: Warm-up label 1

**Another one, worked in full.** The rule decides, not the food.

```text
Request: "I'm pescatarian but shellfish makes me sick"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Lemon Herb Baked Salmon
- 2 salmon fillets (about 6 oz each)
- 1 lemon (for juice and slices)
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- 1 teaspoon dried thyme (or fresh, if available)
- 1 teaspoon dried parsley (or fresh)
- Salt and black pepper to taste
- Fresh dill or parsley for garnish (optional)
[steps cut: checked, nothing in them changes the label]
```

1. **Rule first.** Pescatarian: no meat, but fish and seafood are allowed.
2. **Set aside.** "Shellfish makes me sick" is a wish on top of the rule; the recipe has no shellfish anyway.
3. **The line to test.** "2 salmon fillets".
4. **What it means.** Salmon is a fish. This rule allows fish.
5. **Label: PASS.** The expert: the recipe "uses salmon, which is a type of fish, and does not include any shellfish".
6. **Our note: the dead end.** Treating every animal food the same. Under a vegetarian rule this salmon would FAIL, because vegetarian allows no fish.

Now back to your recipe: under the vegetarian rule, what is a chicken breast, and does the rule allow it?

**Your answer.**

### Key
Kind: show
New: -
Chicken is meat; vegetarian allows no meat, so FAIL. Source of the worked recipe: trace 55_32, PASS, HIGH.

## Help: Label the batch 1

**A worked one on a new surface: the same pasta, a different rule.** (Sent only after the whole batch is marked.)

```text
Request: "Dairy-free but cheese is okay sometimes"
Diet on record: dairy-free
Rule: Dairy-free: No milk, cheese, butter, yogurt, or other dairy products
Recipe: Creamy Tomato Basil Pasta
- 200g (7 oz) spaghetti or your favorite pasta
- 2 tablespoons olive oil
- 3 cloves garlic, minced
- 1 can (14 oz) crushed tomatoes
- 1 teaspoon dried oregano
- 1 teaspoon dried basil (or fresh basil if available)
- 2 tablespoons nutritional yeast (adds cheesy flavor)
- Salt and pepper to taste
- Fresh basil leaves for garnish (optional)
- Red pepper flakes (optional, for a bit of heat)
[steps cut: checked, nothing in them changes the label]
```

1. **Rule first.** Dairy-free: no milk, cheese, butter, yogurt or other dairy.
2. **Set aside.** "Cheese is okay sometimes" is in the request, but the diet on record is dairy-free, so the rule stays strict.
3. **Check every line.** Spaghetti is wheat, not dairy. Nutritional yeast is a yeast with a cheesy taste, not cheese. No line is dairy.
4. **What it means.** No line breaks this rule.
5. **Label: PASS.** The expert: "it uses nutritional yeast to impart a cheesy flavor, which is a common dairy-free alternative".
6. **Our note: the dead end.** Failing it for the spaghetti. Spaghetti breaks a paleo rule, not a dairy-free one.

**Question:** the same spaghetti line sat in your recipe 2. Which rule was it checked against there, and what does that rule say about grains?

**Your answer.**

### Key
Kind: show
New: -
Recipe 2 was paleo, which bans grains, and spaghetti is a grain, so FAIL there; here the rule is dairy-free, so it passes. Source: trace 47_8, PASS, HIGH.

## Help: Label the batch 2

**A worked one on a new surface: the rule allows more than you might think.** (Sent only after the whole batch is marked.)

```text
Request: "I'm pescatarian but I hate fish. Can you give me a seafood pasta recipe?"
Diet on record: pescatarian
Rule: Pescatarian: No meat except fish and seafood
Recipe: Creamy Garlic Shrimp Pasta
- 8 oz (about 225g) linguine or spaghetti
- 2 tablespoons olive oil
- 4 cloves garlic, finely minced
- 1 pound (450g) large shrimp, peeled and deveined
- Salt and freshly ground black pepper, to taste
- 1/2 teaspoon red pepper flakes (optional, for a slight kick)
- 1 cup heavy cream
- 1/2 cup grated Parmesan cheese
- Juice of half a lemon
- Fresh parsley, chopped (for garnish)
- Lemon wedges (for serving)
[steps cut: checked, nothing in them changes the label]
```

1. **Rule first.** Pescatarian: no meat, except fish and seafood. The rule bans nothing else.
2. **Set aside.** "I hate fish" is a wish; the label depends on the rule.
3. **Check every line.** Shrimp (jhinga) is seafood: allowed by name. Cream and Parmesan are dairy: the rule does not ban dairy. Pasta, oil, garlic, lemon, parsley: plants.
4. **What it means.** No line breaks the rule.
5. **Label: PASS.** The expert: "Since the dietary restriction is pescatarian, which allows for seafood but not other meats, the inclusion of shrimp is appropriate."
6. **Our note: the dead end.** Failing it for the cream or the cheese, as if every animal product were banned. Only the vegan rule bans those.

**Question:** in your recipe 5, which words of the pescatarian rule decide the shrimp line, and does the butter line matter?

**Your answer.**

### Key
Kind: show
New: -
"fish and seafood" are allowed, and shrimp is seafood; butter is dairy, which this rule does not ban, so it does not matter: PASS. Source of the worked recipe: trace 10_8, PASS, HIGH.

## Help: Label the batch 3

**A worked one on a new surface: cheese under a vegetarian rule.** (Sent only after the whole batch is marked.)

```text
Request: "Vegetarian protein that isn't beans - I hate beans"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Sweet Potato & Quinoa Stuffed Bell Peppers
- 2 large bell peppers (any color)
- 1 cup quinoa
- 2 medium sweet potatoes, diced
- 1 small red onion, finely chopped
- 2 cloves garlic, minced
- 1 teaspoon paprika
- 1 teaspoon cumin
- Salt and pepper to taste
- 2 tablespoons olive oil
- 1/4 cup crumbled feta cheese (optional)
- Fresh parsley for garnish
[steps cut: checked, nothing in them changes the label]
```

1. **Rule first.** Vegetarian: no meat or fish. The rule itself says dairy and eggs are allowed.
2. **Set aside.** "I hate beans" is a wish; the recipe has no beans anyway.
3. **Check every line.** Peppers, quinoa, sweet potato, onion, garlic, spices, oil, parsley: plants. Feta: cheese, which is dairy.
4. **What it means.** Dairy is allowed by this rule, so no line breaks it.
5. **Label: PASS.** The expert: "the inclusion of feta cheese is acceptable within a vegetarian diet as dairy is allowed".
6. **Our note: the dead end.** Failing it for the cheese, as if every animal product were banned. Only the vegan rule bans those.

**Question:** in your batch, recipe 7 had chicken and recipe 9 had feta, both under the vegetarian rule. Which one breaks it, and which words of the rule tell you?

**Your answer.**

### Key
Kind: show
New: -
Recipe 7 breaks it: chicken is meat ("No meat or fish"). Recipe 9 passes: feta is dairy ("dairy and eggs are allowed"). Source of the worked recipe: trace 57_24, PASS, HIGH.

## Help: Label the batch 4

**A worked one on a new surface: an optional line fails the recipe.** (Sent only after the whole batch is marked.)

```text
Request: "I eat pretty clean most of the time"
Diet on record: whole30
Rule: Whole30: No grains, dairy, legumes, sugar, alcohol, or processed foods
Recipe: Grilled Lemon Herb Chicken Salad
- 2 boneless, skinless chicken breasts
- 1 large lemon (for juice and zest)
- 2 garlic cloves, minced
- Mixed salad greens (about 4 cups)
- 1 cucumber, sliced
- 1 cup cherry tomatoes, halved
- 1 avocado, sliced (optional but adds healthy fats)
- ¼ red onion, thinly sliced
[other salad and herb lines cut: checked, nothing in them changes the label]
For the Dressing:
- 2 tablespoons extra virgin olive oil
- 1 tablespoon lemon juice
- 1 teaspoon honey or maple syrup (optional)
- Salt and pepper to taste
[steps cut: checked, nothing in them changes the label]
```

1. **Rule first.** Whole30 bans grains, dairy, legumes, sugar, alcohol and processed foods. Meat is allowed.
2. **Set aside.** "Clean" is the user's word, not the rule.
3. **Check every line, optional ones too, down to the dressing.** "1 teaspoon honey or maple syrup (optional)".
4. **What it means.** Honey and maple syrup are sugar. Optional still counts: the user may add it.
5. **Label: FAIL.** The expert: "Both honey and maple syrup are not allowed on Whole30 as they are considered added sugars."
6. **Our note: the dead end.** Stopping at the chicken and vegetables, which all fit, and never reading the dressing.

**Question:** your recipe 10 had an optional honey line under a sugar-free rule, and recipe 12 had sugar under a gluten-free rule. Which of the two breaks its own rule, and why?

**Your answer.**

### Key
Kind: show
New: -
Recipe 10: the sugar-free rule bans added sugar, and the optional honey still counts, so FAIL. Recipe 12: the gluten-free rule bans only gluten grains, so the sugar does not matter, PASS. Source of the worked recipe: trace 51_31, FAIL, HIGH.

## Retry

**Ten new recipes, in 3 messages after this one.** Same job as the batch: for each, PASS or FAIL, the deciding line, and sure or not sure. Same food facts. Scored on your matches: you need 8 of the 10, and you must also fail at least 2 of the recipes the expert failed.

Before you see any of them: how many of the 10 do you expect to label the same as the expert?

**Your answer.**

### Key
Kind: scored
Record his prediction as his number times 10: uv run engine.py predict eval-01 <p> --retry. Then send ## Retry 2, ## Retry 3 and ## Retry 4 in order, one per message, with no feedback in between.
Score: none here; the Retry is scored once, after Retry 4.

## Retry 2

For each: PASS or FAIL, the deciding line, and sure or not sure. Steps checked; nothing in them changes a label unless shown.

```text
1. Request: "Comfort food that won't make me feel guilty"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Grilled Chicken and Vegetable Quinoa Bowl
- 1 cup quinoa
- 2 chicken breasts (about 6 oz each)
- 1 red bell pepper
- 1 zucchini
- 1 yellow squash
- 2 tablespoons olive oil
- 1 teaspoon paprika
- 1 teaspoon garlic powder
- Salt and pepper to taste
- Juice of 1 lemon
- Fresh parsley (for garnish, optional)
```
```text
2. Request: "My kid needs a nut-free cookie recipe for school but she's super picky and only likes chocolate"
Diet on record: nut-free
Rule: Nut-free: No tree nuts or peanuts
Recipe: Nut-Free Double Chocolate Cookies (Makes about 12 cookies)
- 1/2 cup (115g) unsalted butter, softened
- 1/2 cup (100g) granulated sugar
- 1/2 cup (100g) packed light brown sugar
- 1 large egg
- 1 teaspoon vanilla extract
- 1 cup (125g) all-purpose flour
- 1/4 cup (25g) unsweetened cocoa powder
- 1/2 teaspoon baking soda
- 1/4 teaspoon salt
- 1 cup (180g) semi-sweet chocolate chips
```
```text
3. Request: "I'm on a sugar-free diet but I want to make candy"
Diet on record: sugar-free
Rule: Sugar-free: No added sugars or high-sugar ingredients
Recipe: Lemon Coconut Bliss Balls
- 1 cup shredded unsweetened coconut
- 1/4 cup almond flour
- 2 tbsp honey or sugar-free syrup (like stevia syrup)
- 1 tbsp freshly squeezed lemon juice
- 1 tsp lemon zest
- 1 tsp vanilla extract
- Pinch of salt
- Optional: a few drops of coconut or lemon extract for more flavor
```
```text
4. Request: "Vegan protein smoothie that doesn't taste chalky"
Diet on record: vegan
Rule: Vegan: No animal products (meat, dairy, eggs, honey, etc.)
Recipe: Vegan Banana Almond Protein Smoothie (Serves 2)
- 2 ripe bananas
- 2 tablespoons almond butter (or any nut butter)
- 1 scoop vegan vanilla protein powder (look for smooth, non-chalky options like pea or rice protein)
- 1 cup almond milk (or any plant-based milk)
- 1/2 teaspoon vanilla extract
- 1 tablespoon chia seeds or hemp seeds (for added nutrients)
- 1 teaspoon maple syrup or agave nectar (optional, for extra sweetness)
- A handful of ice cubes
```

**Your answer.**

### Key
Kind: scored
1 FAIL, chicken is meat (trace 43_14). 2 PASS, no nut or peanut in any line; sugar, butter and flour do not matter to this rule (trace 8_8). 3 FAIL, honey is sugar and an "X or Y" choice counts (trace 26_4). 4 PASS, every line is a plant; maple syrup and agave come from plants (trace 19_36).
Score: count his matches on 1 to 4; the Retry is scored after Retry 4.

## Retry 3

PASS or FAIL, the deciding line, and sure or not sure.

```text
5. Request: "Dairy-free but cheese is okay sometimes"
Diet on record: dairy-free
Rule: Dairy-free: No milk, cheese, butter, yogurt, or other dairy products
Recipe: Garlic Chicken and Veggie Stir-Fry
- 2 boneless, skinless chicken breasts, sliced into thin strips
- 1 cup broccoli florets
- 1 red bell pepper, sliced
- 2 cloves garlic, minced
- 2 tablespoons olive oil
- 1 tablespoon soy sauce or tamari (gluten-free if needed)
- 1 teaspoon honey or maple syrup (optional for a hint of sweetness)
- ¼ cup dairy-free cheese shreds (optional)
- Salt and pepper to taste
- Optional garnish: sliced green onions or sesame seeds
```
```text
6. Request: "Gluten-light recipe - I'm not celiac just sensitive"
Diet on record: gluten-free
Rule: Gluten-free: No wheat, barley, rye, or other gluten-containing grains
Recipe: Zucchini Noodle Primavera
- 2 large zucchinis
- 1 cup cherry tomatoes, halved
- 1 red bell pepper, thinly sliced
- 2 cloves garlic, minced
- 2 tablespoons olive oil
- 1 teaspoon dried oregano
- 1 teaspoon dried basil
- Salt and pepper to taste
- Grated Parmesan cheese (optional, for serving)
- Fresh basil leaves for garnish
Last line: "It pairs wonderfully with a side of crusty gluten-light bread or a fresh green salad."
```
```text
7. Request: "I'm vegan and gluten-free and also hate vegetables. What can I eat?"
Diet on record: vegan
Rule: Vegan: No animal products (meat, dairy, eggs, honey, etc.)
Recipe: Creamy Coconut Lentil Risotto
- 1 cup red lentils
- 1 can (13.5 oz) full-fat coconut milk
- 2 cups vegetable broth (check for gluten-free)
- 1 small onion, finely chopped
- 2 cloves garlic, minced
- 2 tablespoons olive oil
- 1 teaspoon ground turmeric
- 1 teaspoon smoked paprika
- Salt and black pepper to taste
[garnish lines cut: checked, nothing in them changes the label]
```

**Your answer.**

### Key
Kind: scored
5 PASS, honey and chicken are not dairy, and the cheese is sold as dairy-free; "cheese is okay" is a wish (trace 47_3). 6 FAIL, the serving line's bread is wheat, and gluten-light is not gluten-free; the request's "not celiac" does not change the diet on record (trace 48_8). 7 PASS, lentils and coconut milk are plants (trace 29_7).
Score: count his matches on 5 to 7; the Retry is scored after Retry 4.

## Retry 4

The last three. PASS or FAIL, the deciding line, and sure or not sure.

```text
8. Request: "Sugar-free dessert that doesn't taste like sadness"
Diet on record: sugar-free
Rule: Sugar-free: No added sugars or high-sugar ingredients
Recipe: Matcha Coconut Mousse
- 1 can (13.5 oz) full-fat coconut milk or coconut cream
- 2 teaspoons matcha powder (culinary grade for a vibrant flavor)
- 1 teaspoon vanilla extract
- 1 or 2 tablespoons erythritol or monk fruit sweetener (adjust to taste)
- A pinch of salt
- Fresh berries or mint leaves for garnish (optional)
```
```text
9. Request: "Gluten-free pizza dough that actually tastes good and isn't cardboard"
Diet on record: gluten-free
Rule: Gluten-free: No wheat, barley, rye, or other gluten-containing grains
Recipe: Gluten-Free Herb-Infused Pizza Dough
- 1 ½ cups gluten-free all-purpose baking flour (with xanthan gum included, or add ½ teaspoon if not)
- ½ teaspoon salt
- 1 teaspoon sugar
- 1 teaspoon active dry yeast
- 2 tablespoons olive oil
- ¼ cup warm milk (dairy or plant-based)
Tip: "Consider adding a sprinkle of grated Parmesan or a drizzle of honey in the dough for extra richness."
[other lines cut: water and herbs; checked]
```
```text
10. Request: "I want a cheeseburger but I'm dairy-free and vegetarian. I know this sounds impossible but I'm really craving the taste and texture of a classic American cheeseburger and I haven't had one in 3 years since I went vegetarian and developed lactose intolerance"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Dairy-Free Vegetarian "Cheeseburger" (Serves 2)
- 1 can (15 oz) black beans, drained and rinsed
- ½ cup cooked quinoa or cooked oats (for binding)
- 1 tablespoon soy sauce or tamari
- ½ cup raw cashews (soaked in hot water for 20 minutes)
- 2 tablespoons nutritional yeast
- Dairy-free burger buns (look for vegan buns or gluten-free if needed)
[other lines cut: vegetables, spices, oil, toppings; checked, none is meat or fish]
```

**Your answer.**

### Key
Kind: scored
8 PASS, erythritol and monk fruit sweeten with no sugar; berries are fruit (trace 37_33). 9 PASS, the flour is sold gluten-free, and sugar, milk, Parmesan and honey do not matter to a gluten rule (trace 14_22). 10 PASS, beans, grains, cashews and yeast are not meat or fish (trace 24_14). Expert totals for the Retry: 3 FAIL (1, 3, 6), 7 PASS.
Score: Retry = his matches over all 10 recipes, divided by 10, but record Retry=0 if he labelled PASS more than one of the expert's FAILs 1, 3 and 6 (the floor: at least 2 of the 3 caught). Record: uv run engine.py done eval-01 --step "Retry=<v>" --retry.

## Cold

**Seven days on: ten new recipes, in 3 messages after this one.** Same job: for each, PASS or FAIL, the deciding line, and sure or not sure. Same rules and food facts as before. You need 8 of the 10 to match the expert, and you must also fail at least 2 of the recipes the expert failed.

Before you see any of them: how many of the 10 do you expect to label the same as the expert?

**Your answer.**

### Key
Kind: scored
Record his prediction as his number times 10: uv run engine.py predict eval-01 <p> --cold. Then send ## Cold 2, ## Cold 3 and ## Cold 4 in order, one per message, with no feedback in between.
Score: none here; the Cold is scored once, after Cold 4.

## Cold 2

For each: PASS or FAIL, the deciding line, and sure or not sure. Steps checked; nothing in them changes a label unless shown.

```text
1. Request: "I avoid processed foods but I'm lazy"
Diet on record: paleo
Rule: Paleo: No grains, legumes, dairy, refined sugar, or processed foods
Recipe: Garlic Lemon Chickpea Salad (Serves 2)
- 1 can (15 oz) of chickpeas, drained and rinsed
- 1 small cucumber, diced
- 1 small bell pepper (any color), diced
- 2 tablespoons olive oil
- 2 cloves garlic, minced
- Juice of 1 lemon
- Salt and freshly ground black pepper, to taste
- Optional: chopped fresh parsley or mint for garnish
```
```text
2. Request: "Gluten-free birthday cake for my 5-year-old who has celiac but all her friends will be eating regular cake and I don't want her to feel left out"
Diet on record: gluten-free
Rule: Gluten-free: No wheat, barley, rye, or other gluten-containing grains
Recipe: Gluten-Free Vanilla Confetti Cake (Serves 8-10)
- 1 ¾ cups (220g) gluten-free all-purpose flour (blend with xanthan gum if not included)
- 1 ½ teaspoons baking powder (gluten-free)
- ½ cup (115g) unsalted butter, softened
- 1 cup (200g) granulated sugar
- 2 large eggs
- ½ cup (120ml) buttermilk (or milk with 1 tsp lemon juice)
- ½ cup (60g) rainbow sprinkles (make sure they're gluten-free)
[other lines cut: baking soda, salt, vanilla, frosting of butter, powdered sugar and milk; checked, none is a gluten grain]
```
```text
3. Request: "Vegetarian meal that has enough protein for my bodybuilder boyfriend"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Chickpea and Spinach Curry
- 1 can (15 oz) of chickpeas, drained and rinsed
- 2 cups fresh spinach leaves
- 1 medium onion, finely chopped
- 3 cloves garlic, minced
- 1 can (14 oz) diced tomatoes
- 1 tablespoon olive oil
- Salt to taste
Last line: "Serve this hearty chickpea and spinach curry over brown rice or whole-grain naan bread for a balanced, protein-packed meal."
[spice and garnish lines cut: checked, nothing in them changes the label]
```

**Your answer.**

### Key
Kind: scored
1 FAIL, chickpeas are legumes (trace 46_15). 2 PASS, the flour, baking powder and sprinkles are sold gluten-free; butter, sugar, eggs and buttermilk do not matter to a gluten rule (trace 32_33). 3 PASS, no meat or fish; naan and rice do not matter to a vegetarian rule (trace 34_1).
Score: count his matches on 1 to 3; the Cold is scored after Cold 4.

## Cold 3

PASS or FAIL, the deciding line, and sure or not sure.

```text
4. Request: "Dairy-free but cheese is okay sometimes"
Diet on record: dairy-free
Rule: Dairy-free: No milk, cheese, butter, yogurt, or other dairy products
Recipe: Creamy Coconut Curry with Vegetables
- 1 tablespoon coconut oil or vegetable oil
- 1 small onion, finely chopped
- 2 cloves garlic, minced
- 1 medium carrot, sliced
- 1 bell pepper (any color), sliced
- 1 zucchini, sliced
- 1 cup canned chickpeas, drained and rinsed
- 1 can (13.5 oz) coconut milk
- 1 teaspoon curry powder
- Salt and pepper to taste
- Cheese (optional, for topping)
[other spice and garnish lines cut: checked, none is dairy]
```
```text
5. Request: "I'm on a sugar-free diet but I want to make candy"
Diet on record: sugar-free
Rule: Sugar-free: No added sugars or high-sugar ingredients
Recipe: Chocolate Coconut Bites
- 1 cup unsweetened shredded coconut
- 1/4 cup coconut oil
- 2 tablespoons erythritol or monk fruit sweetener (adjust to taste)
- 1 teaspoon vanilla extract
- Pinch of salt
- 2 tablespoons cocoa powder (unsweetened)
Tip: "For added flavor, sprinkle a few crushed nuts or a dash of cinnamon on top before chilling."
```
```text
6. Request: "Vegan protein smoothie that doesn't taste chalky"
Diet on record: vegan
Rule: Vegan: No animal products (meat, dairy, eggs, honey, etc.)
Recipe: Creamy Banana & Berry Vegan Protein Smoothie
- 2 ripe bananas
- 1 cup frozen mixed berries (strawberries, blueberries, raspberries)
- 1 tablespoon chia seeds (optional, for added nutrition)
- 1 tablespoon almond butter or peanut butter
- 2 cups unsweetened almond milk (or any plant-based milk)
- 1 scoop vegan vanilla or berry-flavored protein powder (choose a high-quality one)
- 1 teaspoon maple syrup or agave nectar (optional, for extra sweetness)
- A pinch of cinnamon (optional)
```
```text
7. Request: "Vegetarian curry but I don't eat onions or garlic for religious reasons"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Chickpea and Vegetable Coconut Curry
- 1 can (15 oz) chickpeas, drained and rinsed
- 1 medium carrot, diced
- 1 bell pepper (any color), diced
- 1 zucchini, sliced
- 1 can (13.5 oz) coconut milk
- 1 cup cooked rice or naan for serving
[oil, spice and garnish lines cut: checked, nothing in them changes the label]
```

**Your answer.**

### Key
Kind: scored
4 FAIL, the optional cheese is dairy; the request's "cheese is okay" does not change the diet on record (trace 47_31). 5 PASS, erythritol and monk fruit have no sugar, and nuts do not matter to a sugar rule (trace 26_29). 6 PASS, every line is a plant; maple syrup and agave come from plants (trace 19_3). 7 PASS, no meat or fish (trace 16_19).
Score: count his matches on 4 to 7; the Cold is scored after Cold 4.

## Cold 4

The last three. PASS or FAIL, the deciding line, and sure or not sure.

```text
8. Request: "I eat pretty clean most of the time"
Diet on record: whole30
Rule: Whole30: No grains, dairy, legumes, sugar, alcohol, or processed foods
Recipe: Lemon Herb Grilled Chicken Salad
- 2 boneless, skinless chicken breasts
- 1 tablespoon olive oil
- 4 cups mixed greens (such as spinach, arugula, and romaine)
- 1 cucumber, sliced
- 1 small avocado, sliced (optional)
For the Lemon Herb Dressing:
- Juice of 1 lemon
- 1 teaspoon honey or maple syrup (optional, for a touch of sweetness)
[other salad, dressing and seasoning lines cut: checked, nothing else changes the label]
```
```text
9. Request: "I want a cheeseburger but I'm dairy-free and vegetarian. I know this sounds impossible but I'm really craving the taste and texture of a classic American cheeseburger and I haven't had one in 3 years since I went vegetarian and developed lactose intolerance"
Diet on record: vegetarian
Rule: Vegetarian: No meat or fish, but dairy and eggs are allowed
Recipe: Vegan Lentil Veggie Burger with Dairy-Free Cheese
- 1 cup cooked lentils (green or brown)
- 1/2 cup breadcrumbs (gluten-free if needed)
- 1/4 cup soaked cashews (soaked in hot water for 15 minutes)
- 2 tablespoons nutritional yeast
- 2 gluten-free or whole wheat burger buns
[other lines cut: vegetables, spices, oil, toppings; checked, none is meat or fish]
```
```text
10. Request: "Raw vegan salad that doesn't taste like grass"
Diet on record: raw vegan
Rule: Raw vegan: Vegan foods not heated above 118°F (48°C)
Recipe: Bright Citrus and Nut Raw Vegan Salad
- 1 large orange or blood orange, peeled and segmented
- 1 cup cherry tomatoes, halved
- 1/4 cup red onion, thinly sliced
- 1/4 cup raw walnuts or almonds, roughly chopped
- 2 cups mixed greens (arugula, spinach, or romaine)
- 1 tablespoon extra virgin olive oil
Step 1: "If you prefer a milder onion flavor, soak the slices in cold water for 5 minutes, then drain."
[other lines and steps cut: chopping, mixing and dressing only, no heat]
```

**Your answer.**

### Key
Kind: scored
8 FAIL, honey or maple syrup is sugar and optional still counts (trace 51_23). 9 PASS, lentils, breadcrumbs, cashews and buns are not meat or fish (trace 24_32). 10 PASS, every line is a plant and nothing is heated (trace 9_30). Expert totals for the Cold: 3 FAIL (1, 4, 8), 7 PASS.
Score: Cold = his matches over all 10 recipes, divided by 10, but record Cold=0 if he labelled PASS more than one of the expert's FAILs 1, 4 and 8 (the floor: at least 2 of the 3 caught). Record: uv run engine.py done eval-01 --step "Cold=<v>" --cold.

## Cards

- Q: A recipe calls itself sugar-free and lists honey as optional. The user is sugar-free. Label, and why? | A: FAIL: the title is a claim, and an optional line still counts. || Q: A reply for a paleo user lists "spaghetti or your favorite pasta". Label, and why? | A: FAIL: pasta is made from wheat, a grain, and paleo bans grains.
- Q: The same chicken wrap goes to a vegetarian user and to a nut-free user. The two labels? | A: vegetarian FAIL (chicken is meat), nut-free PASS (no nuts): the label depends on the rule, not the dish. || Q: The same salmon dish goes to a pescatarian user and to a vegetarian user. The two labels? | A: pescatarian PASS (fish allowed), vegetarian FAIL (no fish).
- Q: The request says only "I want to eat healthy". Where do you find the rule to check the recipe against? | A: the diet on record, read before the recipe.
- Q: Every ingredient in a raw vegan soup is a plant. Which part of the reply can still fail it? | A: the cooking steps: heating above the raw limit (frying, boiling) fails it. || Q: Every ingredient of a paleo recipe fits the rule, but the last step says serve it with crusty bread. Label? | A: FAIL: the serving line counts, and bread is a grain.
- Q: You labelled 12 recipes and marked every one PASS. Why can that never pass, even if most of them really were fine? | A: the recipes the expert failed also count on their own: you must fail at least 2 of them, because a failure passed is a user who eats what they must not. || Q: Two labellers each match 10 of 12. One failed 2 of the expert's 3 FAILs, the other failed only 1. Which one passes, and why? | A: the first: the second passed 2 real failures, below the floor of 2 caught, whatever the match count.
