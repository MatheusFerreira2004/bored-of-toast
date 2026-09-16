"""Reusable editorial guides. Content stays readable without JavaScript."""
from html import escape as esc

# ---------------------------------------------------------------------------
# Series definitions — four editorial series for Kitchen Notes
# ---------------------------------------------------------------------------
SERIES = [
    dict(slug='texture-school',    label='Texture School',       desc='How ingredients behave and what to look for.'),
    dict(slug='better-dressings',  label='Better Dressings',     desc='Build and balance a dressing with what you have.'),
    dict(slug='smart-substitutions', label='Smart Substitutions', desc='Understand what changes when you swap an ingredient.'),
    dict(slug='pantry-fixes',      label='Pantry Fixes',         desc='Turn pantry staples into something satisfying.'),
    dict(slug='first-steps', label='First Steps', desc='Start here if the kitchen still feels unfamiliar.'),
    dict(slug='day-one', label='Day One', desc='For absolute beginners: the bare minimum to get started.'),
]

SERIES_SLUG = {s['slug']: s for s in SERIES}

TOPICS = [
    ('prepare', 'Prepare better', 'Small habits before you start.'),
    ('flavor', 'Build flavor', 'Mix, taste, then adjust.'),
    ('swaps', 'Make substitutions', 'Think about what an ingredient does.'),
    ('fixes', 'Fix common mistakes', 'Let texture show you the next move.'),
    ('day-one', 'Day One', 'The absolute bare minimum to survive.'),
]

GUIDES = [
 dict(slug='keep-salad-crisp', title='Keep your salad crisp', topic='Prepare better',
      series='texture-school',
      intro='A little less water. A lot more crunch. Give the ingredients a moment before the dressing goes in.',
      image='keep-salad-crisp.webp', alt='A metal colander with freshly rinsed chickpeas sitting over a ceramic bowl, with a clean folded linen cloth beside it',
      caption='Serving illustration: cucumber and chickpeas keep their shape in a chunky salad.',
      takeaway='Drain → Dry → Dress',
      steps=[('Drain the chickpeas', 'Tip cooked canned chickpeas into a sieve, rinse, then let the water run off.', 'Look underneath: the stream should have slowed to occasional drips.'),
             ('Dry the surfaces', 'Pat the chickpeas gently with a clean towel. Dry washed cucumber and herbs before chopping.', 'Surface water should not collect in the bottom of your mixing bowl.'),
             ('Keep the pieces chunky', 'Cut cucumber into bite-size pieces. If the seed centre is very watery, scoop some out first.', 'Aim for pieces that hold their shape when you toss them.'),
             ('Dress when ready to serve', 'Add a little dressing, toss gently, then decide whether the salad needs more.', 'The ingredients should look lightly coated, with no large puddle underneath.')],
      avoid='Pouring dressing onto ingredients that are still dripping.',
      instead='Drain and dry first. Add the dressing gradually.',
      reason='Extra water dilutes the dressing and collects at the bottom of the bowl.',
      cue='Lift a spoonful: the dressing clings lightly and the cucumber still looks firm.',
      extra_title='Already a little watery?', extra='Lift the salad into a clean bowl with a slotted spoon. Taste before adding more dressing; adding extra oil alone will not remove the water.',
      swap='Out of chickpeas? Cooked white beans can take their place, but fold them in gently because they can be softer. This is a texture change, not an identical result.',
      recipes=[('lemon-chickpea-salad','Lemon chickpea salad'),('smashed-cucumber-edamame-bowl','Cucumber & edamame bowl')]),
 dict(slug='simple-lemon-dressing', title='Make a simple lemon dressing', topic='Build flavor',
      series='better-dressings',
      intro='Whisk, taste, adjust. A good dressing should bring the salad together without hiding the ingredients.',
      image='lemon-dressing.webp', alt='Whisk in a bowl of lemon dressing beside olive oil and a cut lemon',
      caption='Technique illustration: whisk the lemon and oil together before dressing the salad.',
      takeaway='Whisk → Taste → Adjust',
      steps=[('Start with the recipe amounts', 'Put the measured lemon juice and olive oil into a small bowl. Add the seasonings listed in your recipe.', 'Use the recipe as your starting point: lemons vary in sharpness.'),
             ('Whisk until combined', 'Whisk briskly with a fork or small whisk, bringing the oil and lemon juice together.', 'The mixture looks slightly cloudy. It may separate again as it stands.'),
             ('Taste it on an ingredient', 'Dip a piece of cucumber or a chickpea into the dressing. Taste the combination, not just the dressing on its own.', 'You should still taste the vegetable or bean underneath the lemon.'),
             ('Make one small adjustment', 'Too sharp? Whisk in a little more oil. Too oily or flat? Try a little more lemon. Taste again before changing anything else.', 'Whisk once more just before using, then add gradually to the salad.')],
      avoid='Adding several extra ingredients at once to fix the flavor.',
      instead='Change one thing in a small amount, then taste again.',
      reason='Small adjustments make it easier to understand what the dressing needs.',
      cue='On a bite of salad, the dressing tastes bright and rounded rather than overwhelmingly sour or oily.',
      extra_title='Why has the dressing separated?', extra='Oil and lemon juice do not stay mixed on their own. Separation is expected in this simple dressing. Whisk again before pouring; it does not mean the recipe has failed.',
      swap='No lemon? A mild vinegar can provide acidity. Add it gradually and taste: different vinegars have different strengths, so do not assume an identical swap.',
      recipes=[('lemon-chickpea-salad','Lemon chickpea salad'),('mediterranean-warm-green-lentils','Warm green lentils')]),
 dict(slug='make-beans-creamy', title='Make beans creamy', topic='Fix common mistakes',
      series='pantry-fixes',
      intro='Keep most of the beans whole. Mash a few. Let a little liquid turn them into a spoonable skillet meal.',
      image='make-beans-creamy.webp', alt='A skillet partially filled with white beans in a light sauce, a wooden spoon actively pressing and mashing a few beans against the pan',
      caption='Serving illustration: whole beans sit in a sauce with enough body to coat them.',
      takeaway='Warm → Mash → Loosen',
      steps=[('Warm the cooked beans', 'Follow your recipe to soften the aromatics, then add cooked beans and the starting amount of liquid.', 'These notes are for canned or already cooked beans, not dried beans.'),
             ('Mash a small spoonful', 'Press a few beans against the side of the pan with your spoon, then stir them back into the liquid.', 'You should still see plenty of whole beans in the pan.'),
             ('Watch the sauce', 'Simmer gently, stirring occasionally. If the mixture catches or looks dry, add a small splash of water.', 'The sauce should move when stirred, rather than sit as a stiff paste.'),
             ('Adjust before serving', 'Too loose? Simmer a little longer. Too thick? Stir in another small splash. Follow the recipe for greens and finishing seasonings.', 'Check again just before serving: the sauce can thicken as it stands.')],
      avoid='Adding a large amount of water, then mashing all the beans to compensate.',
      instead='Start with the recipe amount and adjust with small splashes.',
      reason='You keep control of the sauce while preserving the texture of whole beans.',
      cue='Drag a spoon through the pan: the sauce slowly flows back into the gap and coats the beans.',
      extra_title='Still thin after stirring?', extra='Give the pan a little more gentle simmering time, uncovered, and reassess. If needed, mash a few more beans. Pan width and heat affect how quickly liquid evaporates.',
      swap='Using chickpeas instead? They tend to stay firmer than white beans. Expect a chunkier result and mash a few deliberately rather than waiting for them to soften into the sauce.',
      recipes=[('lemon-white-bean-skillet','Lemony white beans & spinach'),('garlic-butter-bean-mushroom-toast','White bean & mushroom toast')]),
 dict(slug='read-it-twice', title='Read it twice before you touch a pan', topic='Prepare better',
      series='first-steps',
      intro="The most common beginner mistake happens before the stove is even on. Read the whole recipe once for the plan, then once for the order.",
      image='read-the-recipe.webp', alt='An open recipe notebook beside a pencil and a small notepad',
      caption='Illustration: a recipe read start to finish before anything is chopped.',
      takeaway='Read → Picture → Then start',
      steps=[('Read the whole thing once', 'Go top to bottom before touching anything — ingredients, then every step, including the ones near the end.', 'You should be able to say out loud what the finished dish looks like.'),
             ('Picture the order', 'Notice which steps happen at the same time. Some things wait on the counter while others are on the stove.', 'If two steps say "at the same time," you have a plan for both hands.'),
             ('Get everything out first', 'Pull every ingredient and tool onto the counter before turning on any heat.', 'The counter has what the recipe needs and nothing you have to search for mid-step.'),
             ('Start when you are not surprised', 'Begin cooking once nothing on the page can catch you off guard.', 'The next step is never a surprise — you already read it.')],
      avoid='Starting to cook after only skimming the ingredient list.',
      instead='Read every step before the pan goes on the heat.',
      reason='A recipe read halfway through hides its timing — you find out too late that something needed to happen earlier.',
      cue='You can describe the last step before you have done the first one.',
      extra_title='Still feels like too much to remember?',
      extra='Keep the page open and glance at it between steps. Reading it once is about knowing the shape of the recipe, not memorizing it.',
      swap='This habit works on every recipe, not just the ones on this site — only how much there is to read changes.',
      recipes=[('lemon-white-bean-skillet','Lemony white beans & spinach'), ('garlic-butter-bean-mushroom-toast','White bean & mushroom toast')]),
 dict(slug='what-the-pan-tells-you', title='What the pan is trying to tell you', topic='Build flavor',
      series='first-steps',
      intro="Medium heat isn't a number on a dial — it's something you can see and hear. Learn the signs instead of guessing.",
      image='pan-heat-cue.webp', alt='A skillet on the stove with oil beginning to shimmer',
      caption='Illustration: oil at the point where it starts to shimmer, not smoke.',
      takeaway='Shimmer → Sizzle → Adjust',
      steps=[('Warm the pan before the oil', 'Put the empty pan on medium heat for a minute before adding oil.', 'Hold your hand a few inches above it — you should feel gentle warmth, not intense heat.'),
             ('Watch the oil, not the clock', 'Add the oil and wait for it to move like water and catch a faint shimmer.', 'It looks loose and glossy, with no wisps of smoke rising from it.'),
             ('Listen for the sizzle', 'Add the first ingredient and listen. A steady, active sizzle means the pan is ready.', 'It sounds like light rain, not a sharp crackle and not silence.'),
             ('Adjust without starting over', 'Too quiet? Wait a little longer. Too loud, or something is browning too fast? Lower the heat — you do not need to remove the pan.', 'The sizzle settles into a steady, even sound within a few seconds.')],
      avoid='Turning the heat to high to save time.',
      instead='Start at medium and let the pan tell you when to adjust.',
      reason='High heat cooks the outside before the inside catches up, and leaves very little time to notice a mistake.',
      cue='The oil shimmers and the pan sizzles steadily — nothing is smoking, popping violently, or silent.',
      extra_title='Smoke coming off the pan?',
      extra='Take it off the heat for a moment. Smoking oil is a sign the pan is hotter than the recipe needs, not a sign to keep going.',
      swap='This works the same on nonstick, stainless, or cast iron — only how quickly the pan heats up differs.',
      recipes=[('lemon-white-bean-skillet','Lemony white beans & spinach'), ('mediterranean-warm-green-lentils','15-minute Mediterranean warm green lentils')]),
 dict(slug='taste-then-decide', title='Taste, then decide', topic='Fix common mistakes',
      series='first-steps',
      intro="When something tastes off, most people panic and start dumping in random ingredients. There's a simpler order: salt, then acid, then fat.",
      image='taste-then-decide.webp', alt='A tasting spoon beside three small bowls of salt, lemon, and olive oil',
      caption='Illustration: three small adjustments, tasted one at a time.',
      takeaway='Salt → Acid → Fat',
      steps=[('Taste it plain first', 'Before adding anything, taste a spoonful on its own and notice what feels missing.', 'You can describe it in one word: flat, dull, heavy, or sharp.'),
             ('Try salt first', 'A small pinch, stirred in, tasted again. Salt usually solves "flat" before anything else does.', 'Other flavors suddenly taste more like themselves, not just saltier.'),
             ('Reach for acid next', 'If it still tastes heavy or dull after salt, try a small squeeze of lemon or splash of vinegar.', 'The dish tastes brighter and lighter, like something lifted off it.'),
             ('Finish with fat if it needs rounding out', 'Still tastes sharp or thin? A little olive oil, butter, or cheese can round it out.', 'The flavors feel connected instead of separate.')],
      avoid='Adding several ingredients at once to fix a vague "something is missing" feeling.',
      instead='Change one thing in a small amount, taste, then decide on the next.',
      reason='Fixing three things at once makes it impossible to know which one actually worked — or to undo it if you go too far.',
      cue='You can name what changed after each adjustment, not just that "it tastes better now."',
      extra_title='Still tastes off after all three?',
      extra="That's useful information too — it might need more of the main ingredient or more time to cook, not something new.",
      swap='This order works on almost anything you cook — it is a way of tasting, not a technique tied to one recipe.',
      recipes=[('lemon-chickpea-salad','Lemon chickpea salad'), ('smashed-cucumber-edamame-bowl','Smashed cucumber, avocado & edamame crunch bowl')]),

 dict(slug='how-to-brown-mushrooms', title='How to actually brown mushrooms', topic='Fix common mistakes',
      series='texture-school',
      intro='The secret to golden mushrooms isn\'t just the heat, it\'s patience. Leave them alone.',
      image='brown-mushrooms.webp', alt='Watercolor illustration of mushrooms browning in a hot skillet in a single layer',
      caption='Illustration: a single layer of mushrooms browning without being crowded.',
      takeaway='Heat → Space → Patience',
      steps=[('Get the pan hot', 'Warm your skillet over medium-high heat with butter or oil until it\'s shimmering.', 'The pan needs to be hot enough to sear the mushrooms the moment they touch it.'),
             ('Leave space between them', 'Add the mushrooms in a single layer. Do not pile them on top of each other.', 'If they are crowded, they will steam in their own juices and turn gray and rubbery.'),
             ('Do nothing for 3 minutes', 'Walk away or just watch. Do not stir them. Let them sit perfectly still.', 'You will hear the sound change from a wet sizzle to a drier crackle as the moisture cooks off.'),
             ('Stir and finish', 'Once the bottom is deeply golden, give them a stir to cook the other side for a minute or two.', 'They should look deeply browned and shrunk, not swimming in liquid.')],
      avoid='Dumping a huge pile of mushrooms into a cold pan and stirring constantly.',
      instead='Use a hot pan, a single layer, and do not touch them for the first few minutes.',
      reason='Mushrooms are full of water. Stirring them constantly releases that water, boiling them instead of searing them.',
      cue='The sound changes from a wet hiss to a sharp fry, and the edges look deeply caramelized.',
      extra_title='Too much liquid in the pan?', extra='If you accidentally crowded them and they released a pool of water, don\'t panic. Just keep cooking until all that water evaporates. They will eventually brown, it just takes longer.',
      swap='This rule applies to browning almost anything—zucchini, tofu, or meat. Space and patience create a sear.',
      recipes=[('garlic-butter-bean-mushroom-toast','Garlic butter bean & mushroom toast')]),

 dict(slug='the-garlic-timeline', title='The garlic timeline', topic='Build flavor',
      series='first-steps',
      intro='Garlic cooks quickly and burns even faster. It needs gentle heat and attention, not a screaming hot pan.',
      image='lemon-white-bean-skillet-garlic.webp', alt='Watercolor illustration of sliced garlic gently sizzling in a skillet of olive oil',
      caption='Illustration: garlic sizzling gently in oil, pale and fragrant.',
      takeaway='Gentle heat → Fragrant → Stop',
      steps=[('Start with warm oil', 'Drop your chopped or sliced garlic into oil that is warm, not smoking hot.', 'You want a gentle, steady sizzle, not an aggressive pop and crackle.'),
             ('Watch the color closely', 'Stir the garlic continuously. You are looking for it to become pale golden and fragrant, which takes about 30 to 60 seconds.', 'Do not walk away. Garlic can go from perfect to burnt in ten seconds.'),
             ('Stop the cooking', 'The moment it smells amazing and is lightly golden, immediately add the next wet ingredient (like beans, broth, or tomatoes).', 'The liquid drops the temperature of the pan instantly, stopping the garlic from browning further.')],
      avoid='Throwing garlic into a very hot pan at the same time as onions.',
      instead='Cook onions first, then add garlic for the last minute, or use gentle heat.',
      reason='Onions take 5-10 minutes. Garlic takes 1 minute. If they go in together on high heat, the garlic will burn and turn bitter.',
      cue='Your kitchen smells intensely of savory garlic, and the pieces are pale blond, not dark brown.',
      extra_title='What if it burned?', extra='If your garlic turns dark brown or black, throw it out, wipe the pan, and start over. Burnt garlic will make the entire dish taste unpleasantly bitter, and no amount of seasoning will fix it.',
      swap='If you are using garlic powder instead of fresh, it goes in with the dry spices, not sizzling in the oil on its own.',
      recipes=[('lemon-white-bean-skillet','Lemony white beans & spinach'), ('mediterranean-warm-green-lentils','Mediterranean warm green lentils')]),

 dict(slug='swapping-herbs', title='Swapping herbs without ruining the dish', topic='Make substitutions',
      series='smart-substitutions',
      intro='Hard herbs like the heat early on. Soft herbs prefer to join the party right at the end.',
      takeaway='Hard early → Soft late → Taste',
      steps=[('Identify your herb', 'Look at the stem. Is it woody like a twig (rosemary, thyme, oregano)? Or is it soft and green (basil, parsley, cilantro)?', 'Woody herbs are "hard". Green, leafy ones are "soft".'),
             ('Cook hard herbs early', 'Add rosemary or thyme while cooking aromatics (like onions) so the heat can extract their flavor.', 'They hold up well to heat and flavor the whole dish over time.'),
             ('Fold soft herbs late', 'Stir basil, parsley, or cilantro in right before serving.', 'Heat destroys their delicate flavor and turns them brown.')],
      avoid='Swapping a hard herb for a soft herb in the middle of a 30-minute simmer.',
      instead='Match the category (hard for hard, soft for soft), or change WHEN you add it.',
      reason='Rosemary is aggressive and thrives on heat. Basil is delicate and dies on heat.',
      cue='The herbs smell fresh and vibrant when you taste the dish.',
      extra_title='Dried vs Fresh?', extra='Dried herbs are concentrated. Use 1 teaspoon of dried herbs for every 1 tablespoon of fresh. Always add dried herbs early in the cooking process so they can rehydrate.',
      swap='If a recipe wants fresh parsley and you only have dried oregano, use a tiny pinch of the oregano early on, rather than a handful at the end.',
      recipes=[('crispy-sheet-pan-gnocchi','Crispy sheet pan gnocchi'), ('garlic-butter-bean-mushroom-toast','Garlic butter bean & mushroom toast')]),

 dict(slug='three-tools', title='The only 3 tools you actually need', topic='Day One',
      series='day-one',
      intro='You do not need a 12-piece knife block or copper pots. You need three things to make 90% of meals.',
      image='read-the-recipe.webp', alt='A simple chef knife, a wooden cutting board, and a non-stick skillet',
      caption='Illustration: a chef knife, a cutting board, and a skillet.',
      takeaway='Knife → Board → Pan',
      steps=[('A Chef\'s Knife', 'An 8-inch chef\'s knife is all you need. Do not buy a set. Spend your budget on one good knife that feels comfortable to hold.', 'It should feel balanced in your hand, not too heavy.'),
             ('A Large Cutting Board', 'A big wooden or plastic board. Small boards make chopping frustrating and dangerous because food rolls off.', 'The board should be wider than your knife.'),
             ('A 10-inch Skillet', 'A non-stick or stainless steel skillet with a lid. It fries eggs, simmers sauces, and toasts nuts.', 'It should be large enough that food has space to breathe.'),
             ('Skip the gadgets', 'Garlic presses, egg slicers, and avocado tools are unnecessary. Your knife does all of this.', 'A clean drawer with fewer tools is better than a cluttered one.')],
      avoid='Buying a massive block of knives and tools you will never use.',
      instead='Buy three high-quality essentials.',
      reason='More tools just mean more things to wash and lose track of.',
      cue='You can cook an entire meal without reaching for a special gadget.',
      extra_title='What about pots?',
      extra='A medium pot for boiling pasta or rice is helpful, but if you only have a deep skillet, you can survive your first week.',
      swap='Any heavy pan works if you do not have a skillet, but a skillet makes tossing and flipping much easier.',
      recipes=[('lemon-white-bean-skillet','Lemony white beans & spinach')]),

 dict(slug='pantry-zero', title='What to buy to not starve', topic='Day One',
      series='day-one',
      intro='An empty fridge is intimidating. Here are the 5 ingredients that guarantee you can always make dinner.',
      image='read-the-recipe.webp', alt='A simple pantry shelf with pasta, beans, garlic, oil, and salt',
      caption='Illustration: the foundational pantry items.',
      takeaway='Oil → Salt → Base',
      steps=[('Olive Oil and Salt', 'These are the non-negotiables. Food without salt tastes like nothing, and food without oil sticks to the pan.', 'Kosher salt is easier to pinch and measure than table salt.'),
             ('Pasta or Rice', 'A cheap, shelf-stable base that fills you up. It acts as a blank canvas for whatever else you have.', 'Dried pasta lasts essentially forever.'),
             ('Canned Beans', 'Chickpeas or white beans. They are cheap, healthy, already cooked, and ready to eat immediately.', 'Rinse them before using to remove the starchy liquid.'),
             ('Garlic and Lemons', 'The flavor makers. Garlic makes everything smell like a real meal, and lemon wakes up flat flavors.', 'Keep garlic in a dark, dry place, not the fridge.')],
      avoid='Buying exotic ingredients for one specific recipe and letting them rot.',
      instead='Stock a foundational pantry that can build dozens of meals.',
      reason='If you have pasta, garlic, and oil, you have dinner.',
      cue='You can open a bare cupboard and still see a meal waiting to happen.',
      extra_title='What about protein?',
      extra='Eggs are the perfect beginner protein: cheap, fast, and they last weeks in the fridge.',
      swap='If you hate beans, keep a bag of frozen peas or frozen spinach. They defrost in minutes and add color and nutrition.',
      recipes=[('lemon-chickpea-salad','Lemon chickpea salad')]),

 dict(slug='how-to-hold-a-knife', title='How to hold a knife and not get hurt', topic='Day One',
      series='day-one',
      intro='Do not hold the food with flat fingers. Learn the claw grip so the knife rests against your knuckles, not your fingertips.',
      image='read-the-recipe.webp', alt='Illustration of hands using the claw grip to chop an onion',
      caption='Illustration: the claw grip protects your fingertips.',
      takeaway='Pinch → Claw → Slice',
      steps=[('Pinch the blade', 'Do not grip the handle like a baseball bat. Pinch the base of the blade with your thumb and index finger.', 'You have much more control over the tip of the knife this way.'),
             ('Make a claw', 'Tuck the fingertips of your other hand inward, like a bear claw. Rest your knuckles against the side of the blade.', 'Your fingertips are completely hidden and safe.'),
             ('Slice, do not chop', 'Move the knife in a forward and downward circle, like a locomotive wheel. Do not aggressively hack straight down.', 'The sharp edge slices smoothly without needing a lot of force.'),
             ('Stabilize the board', 'Put a damp paper towel under your cutting board so it does not slide around.', 'The board should feel cemented to the counter.')],
      avoid='Laying your fingers flat on the food while cutting.',
      instead='Tuck your fingertips away into the claw grip.',
      reason='A knife resting against flat fingers is an accident waiting to happen.',
      cue='The side of the blade gently glides against your knuckles as you slice.',
      extra_title='Knife feels dull?',
      extra='A dull knife is more dangerous than a sharp one because you have to push harder, increasing the chance of slipping.',
      swap='If you are cutting something round like an onion, slice it in half first so it lays flat and stable on the board.',
      recipes=[('smashed-cucumber-edamame-bowl','Smashed cucumber bowl')]),
]


def url(g): return '/kitchen-notes/' + g['slug'] + '/'

def figure(g):
    if not g.get("image"): return ""
    return f'<figure class="kn-photo"><img src="/assets/{g["image"]}" alt="{esc(g["alt"], quote=True)}" width="800" height="600" decoding="async"><figcaption>{g["caption"]} Image is AI-generated.</figcaption></figure>'

def series_badge(g, as_link=True):
    s = SERIES_SLUG.get(g.get('series', ''))
    if not s:
        return ''
    if as_link:
        return f'<a class="kn-series-badge" href="/kitchen-notes/#{s["slug"]}">{esc(s["label"])}</a>'
    return f'<span class="kn-series-badge">{esc(s["label"])}</span>'

def guide(g):
    steps=''.join(f'<li><span class="kn-number">{i:02}</span><div><h3>{title}</h3><p>{action}</p><p class="kn-cue"><strong>Look for</strong> {cue}</p></div></li>' for i,(title,action,cue) in enumerate(g['steps'],1))
    links=''.join(f'<a class="kn-recipe-link" href="/recipes/{slug}/">{title}<span aria-hidden="true"> ↗</span></a>' for slug,title in g['recipes'])
    badge = series_badge(g)
    next_guide = GUIDES[(GUIDES.index(g)+1)%len(GUIDES)]
    return f'''<article class="kn-page wrap">
<a class="breadcrumb" href="/kitchen-notes/">← All kitchen notes</a>
<header class="kn-hero" {'' if g.get('image') else 'style="grid-template-columns: 1fr;"'}><div {'' if g.get('image') else 'style="max-width: 800px; margin: 0 auto;"'}>{badge}<p class="eyebrow">KITCHEN NOTES / {g['topic'].upper()}</p><h1>{g['title']}</h1><p class="kn-lead">{g['intro']}</p><div style="margin: 30px 0;"><span class="kn-hand">{g['takeaway']}</span></div><a class="text-link" href="#guide-steps">Go to the technique ↓</a></div>{figure(g)}</header>
<div class="kn-guide-layout"><section id="guide-steps"><p class="eyebrow">THE SMALL DETAILS THAT HELP</p><h2>Here's how.</h2><ol class="kn-steps">{steps}</ol></section>
<aside class="kn-margin"><span class="kn-hand">A note worth keeping</span><h2>Know what to look for.</h2><p>{g['cue']}</p><a class="text-link" href="#put-it-to-work">Try it in a recipe ↓</a></aside></div>
<section class="kn-comparison" aria-label="Common mistake and better approach"><div><p class="eyebrow">AVOID THIS</p><h2>{g['avoid']}</h2><p>{g['reason']}</p></div><div><p class="eyebrow">TRY THIS INSTEAD</p><h2>{g['instead']}</h2></div></section>
<section class="kn-extras"><div><p class="eyebrow">MAKE SUBSTITUTIONS</p><h2>Keep the job. Expect a change.</h2><p>{g['swap']}</p></div><details><summary>{g['extra_title']}</summary><p>{g['extra']}</p></details></section>
<section id="put-it-to-work" class="kn-related"><p class="eyebrow">FROM NOTEBOOK TO TABLE</p><h2>Put it to work.</h2>{links}<p class="kn-small">Linked recipes are development editions and await kitchen testing. These guides do not change that status.</p></section>
<nav class="kn-next" aria-label="More kitchen notes"><a class="text-link" href="/kitchen-notes/">← Back to the notebook</a><a class="text-link" href="{url(next_guide)}">Read another technique ↗</a></nav>
</article>'''

def index():
    nav=''.join(f'<a href="#{slug}">{title}</a>' for slug,title,_ in TOPICS)

    # Series navigation
    series_nav = ''.join(
        f'<a class="kn-series-pill" href="/kitchen-notes/#{s["slug"]}" id="kn-series-{s["slug"]}">'
        f'<strong>{esc(s["label"])}</strong>'
        f'<span>{esc(s["desc"])}</span>'
        f'</a>'
        for s in SERIES
    )

    cards=''.join(f'<a class="kn-guide-card" href="{url(g)}"><span class="eyebrow">0{i} / {g["topic"].upper()}</span>{series_badge(g, as_link=False)}<h3>{g["title"]}</h3><p>{g["intro"]}</p><span class="text-link">Read the guide ↗</span></a>' for i,g in enumerate(GUIDES,1))

    topics=''.join(f'<section class="kn-topic" id="{slug}"><p class="eyebrow">{i:02} / {title.upper()}</p><h2>{desc}</h2><p>{body}</p><a class="text-link" href="{href}">{label} ↗</a></section>' for i,(slug,title,desc,body,href,label) in enumerate([
      (*TOPICS[0], 'Drain and dry before dressing. A few moments of preparation can make the finished salad feel quite different.',url(GUIDES[0]),'Keep your salad crisp'),
      (*TOPICS[1], 'Taste a dressing with the food it will go on, then adjust one thing at a time.',url(GUIDES[1]),'Make a lemon dressing'),
      (*TOPICS[2], 'Think about texture, acidity and the role an ingredient plays. Each technique guide includes a substitution note; our original notebook explores three ways to use chickpeas.','/kitchen-notes/','One can, three directions'),
      (*TOPICS[3], 'Too thin or too thick? Learn the signs before adding more ingredients.',url(GUIDES[2]),'Make beans creamy'),
    ],1))

    return f'''<div class="kn-page wrap"><header class="kn-index-header"><p class="eyebrow">THE KITCHEN NOTEBOOK</p><h1>Small lessons.<br><em>Better lunches.</em></h1><p class="kn-lead">A few useful things to know before you reach for another recipe. Practical guides for the ingredients already in your kitchen.</p></header>
<nav class="kn-topics" aria-label="Kitchen note topics">{nav}</nav>
<section class="kn-feature"><div><p class="eyebrow">START WITH ONE SMALL CHANGE</p><h2>A crisp salad starts<br>before the dressing.</h2><p>Give the water somewhere else to go. Learn what to drain, what to dry, and when to toss.</p><a class="button" href="{url(GUIDES[0])}">Read the crisp-salad guide ↗</a></div>{figure(GUIDES[0])}</section>
<section class="kn-library"><p class="eyebrow">THREE TECHNIQUES TO KEEP</p><h2>Open a note.</h2><div class="kn-card-grid">{cards}</div></section>
<section class="kn-series" aria-label="Browse by series">
  <p class="eyebrow">BROWSE BY SERIES</p>
  <h2>Pick a theme.</h2>
  <div class="kn-series-grid">{series_nav}</div>
  <p class="kn-series-note">New guides are added to each series as the notebook grows.</p>
</section>
<div class="kn-topic-grid">{topics}</div><div class="kn-ending"><span class="kn-hand">Curiosity is a useful ingredient.</span><a class="text-link" href="/recipes/">Find something to make ↗</a></div></div>'''

def home_feature():
    return f'''<section class="kn-home wrap"><div class="kn-home-main"><div><p class="eyebrow">02 / A NOTE FROM THE KITCHEN</p><h2>A little know-how.<br><em>A better lunch.</em></h2><p>Keep your salad crisp with three small habits: drain well, dry the surfaces, and dress when you're ready to eat.</p><a class="button" href="{url(GUIDES[0])}">Keep your salad crisp ↗</a></div>{figure(GUIDES[0])}</div><div class="kn-home-links"><span class="kn-hand">While you're here…</span><a href="{url(GUIDES[1])}">Make a lemon dressing ↗</a><a href="{url(GUIDES[2])}">Make beans creamy ↗</a><a class="text-link" href="/kitchen-notes/">All kitchen notes ↗</a></div></section>'''

def start():
    return f'''<article class="kn-page wrap" style="max-width: 800px; padding-bottom: 80px;">
    
    <header style="padding-top: 60px; margin-bottom: 50px;">
        <h1 style="font-size: clamp(3rem, 6vw, 4.5rem);">You don't need a plan.<br>You need one small win.</h1>
        <p class="hero-note kn-hand" style="margin-top: 10px;">Everyone starts somewhere — even us.</p>
        <p class="lead" style="margin-top: 30px; color: var(--ink);">No 12-step guides here. Just enough to get a good meal on the table tonight, and a little more confidence than you had this morning.</p>
    </header>
    
    <figure style="margin-bottom: 60px;">
        <img src="/assets/read-the-recipe.webp" alt="An open recipe notebook page with visible handwriting-style text blocks, a pencil resting diagonally across it, a small folded linen napkin nearby." style="width: 100%; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    </figure>
    
    <style>
    .notebook-path {{
        fill: none;
        stroke: var(--accent, #b8860b);
        stroke-width: 3;
        stroke-dasharray: 8 10;
        stroke-linecap: round;
    }}
    @media (prefers-reduced-motion: no-preference) {{
        .notebook-path {{
            stroke-dasharray: 1000;
            stroke-dashoffset: 1000;
            animation: drawNotebookPath 2.5s ease-out forwards;
        }}
        @keyframes drawNotebookPath {{
            to {{ stroke-dashoffset: 0; }}
        }}
    }}
    .guide-step-link {{
        font-family: 'DM Serif Display', serif;
        font-size: 1.8rem;
        color: var(--heading-color);
        line-height: 1.2;
        border: none;
        text-decoration: none;
    }}
    .guide-step-link:hover {{
        color: var(--brand-blue);
    }}
    .path-container {{
        position: relative;
        padding: 40px 0;
        margin: 60px auto;
        max-width: 600px;
        display: flex;
        flex-direction: column;
        gap: 90px;
    }}
    .path-node {{
        display: flex;
        align-items: center;
        gap: 15px;
        position: relative;
        z-index: 1;
    }}
    .path-dot {{
        width: 14px;
        height: 14px;
        background-color: var(--heading-color);
        border-radius: 50%;
        flex-shrink: 0;
    }}
    </style>
    
    <div class="path-container">
        <svg width="100%" height="100%" style="position: absolute; top:0; left:0; pointer-events: none; z-index: 0;" preserveAspectRatio="none" viewBox="0 0 100 100">
            <path class="notebook-path" d="M 12 10 Q 70 50 88 90" vector-effect="non-scaling-stroke"/>
        </svg>
        
        <div class="path-node" style="align-self: flex-start; padding-left: 5%;">
            <div class="path-dot"></div>
            <a class="guide-step-link" href="/kitchen-notes/read-it-twice/">Read it twice before you touch a pan ↗</a>
        </div>
        
        <div class="path-node" style="align-self: center;">
            <div class="path-dot"></div>
            <a class="guide-step-link" href="/kitchen-notes/what-the-pan-tells-you/">What the pan is trying to tell you ↗</a>
        </div>
        
        <div class="path-node" style="align-self: flex-end; padding-right: 5%; flex-direction: row-reverse; text-align: right;">
            <div class="path-dot"></div>
            <a class="guide-step-link" href="/kitchen-notes/taste-then-decide/">Taste, then decide ↗</a>
        </div>
    </div>
    
    <div style="text-align: center; margin: 80px 0;">
        <span class="kn-hand" style="font-size: 2rem;">Curiosity is a useful ingredient.</span>
    </div>
    
    <section style="margin-top: 60px; padding-top: 40px; border-top: 1px solid var(--line);">
        <p class="eyebrow">YOUR FIRST VICTORY</p>
        <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
            <a class="text-link" href="/recipes/lemon-chickpea-salad/" style="font-size: 1.2rem;">Lemon chickpea salad ↗</a>
            <a class="text-link" href="/recipes/blueberry-overnight-oats/" style="font-size: 1.2rem;">Blueberry overnight oats ↗</a>
        </div>
    </section>
    
    </article>'''
