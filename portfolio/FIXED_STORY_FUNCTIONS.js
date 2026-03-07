// PASTE THESE FUNCTIONS INTO loaded_bones.html (lines 2851-2997)
// These replace the broken functions with properly quoted strings

function showShipTutorialIntro() {
  const screen = document.getElementById('story-screen');
  const para1 = translateVisibleText("The sea air blows around you as you watch the waves break against your ship. You hoped to make it to your destination without any storms, but it seems luck is not on your side. The sea churns and grows violent as you sail under the rolling black clouds. You've never seen clouds quite so dark. If you weren't on the open ocean, you'd think it was smoke.");
  const para2 = translateVisibleText("The deck lurches, as though colliding with a rock, but as the captain orders the sailors about, you take a peek over the side and find nothing that could have caused the movement, just the shadows of marine life zipping around the beleaguered boat. But they're too fast. A loud splash sounds, and you whip around to see a silhouette behind you. A sailor you've never met stands, sword drawn, dripping wet. It opens its mouth, letting out a low whistle, before raising its blade and charging you.");
  screen.innerHTML = `
    <div style="max-width:760px;margin:0 auto;">
      <div class="story-text">${para1}</div>
      <div class="story-text">${para2}</div>
      <div style="margin-top:30px;text-align:center;">
        <button class="btn primary" onclick="startShipTutorialCombat()">${translateVisibleText('Fight')}</button>
      </div>
    </div>
  `;
  showScreen('story-screen');
}

function showShipAftermath(result) {
  const screen = document.getElementById('story-screen');
  const victoryText = translateVisibleText('You stand over the defeated pirate. The strange man looks up at you, then begins to... melt. He disappears, seeping into the cracks in the boards of the ship, leaving you alone. Truly alone, because as you look around, you can find none of the other sailors manning the ship. The storm has calmed, but the clouds still fill the sky. The sea is eerily still. Then you feel something. A terrible rumbling, growing all around you. The ship explodes beneath your feet, and you are sent sailing into the air. You manage to get a look at a massive creature, a sea serpent of some kind, emerging from where you were just standing, before you collide with the water and everything goes black');
  const defeatText = translateVisibleText('You lie on your back, defeated. You try to inch away from the strange pirate, but with the rail behind you and his blade before you, you have nowhere to go. A rumbling sounds all around the ship, and the pirate finally takes its unearthly dark eyes off you as it looks around frantically. You take the chance to scramble to the side and put some distance between you and your foe. You grab a sturdy chunk of wood as a primitive defensive club, but when you turn around you witness the pirate diving off the side of the ship. You rush to the side to see where he went, but despite searching for a few minutes you see nothing. You turn around and are faced with something infinitely worse. A massive sea serpent, 300, no 400 feet tall at least, looms above your ship, huge glowing blue eyes focused unblinking at you. Your head begins to swim, and you collapse against the rail for support. The eyes seem to grow in both size and intensity, and soon you can see nothing else. You try to turn, but are unable to escape the blue light. Soon, your mind collapses, and the world flees from you.');
  const selected = result === 'victory' ? victoryText : defeatText;

  screen.innerHTML = `
    <div style="max-width:760px;margin:0 auto;">
      <div class="story-text">${selected}</div>
      <div style="margin-top:30px;text-align:center;">
        <button class="btn primary" onclick="showCrashMemoryScene()">${translateVisibleText('Continue')}</button>
      </div>
    </div>
  `;
  showScreen('story-screen');
}

function showLakeWakeScene() {
  const screen = document.getElementById('story-screen');
  const para1 = translateVisibleText("As life slowly awakens in your head, you feel coarse sand beneath you and the gentle nudging of waves against your leg. Your first attempt to move your arms fails you, but after a few moments you're able to place them underneath you and shakily stand. You see the wide golden expanse of plains ahead.");
  const para2 = translateVisibleText("You brush off some of the sand and turn to see what's left of the crash. However...");
  const para3 = translateVisibleText('You are not on a seaside beach or some lonely island.');
  const para4 = translateVisibleText('Before you is a lake. A large lake, to be sure, but you scan the breadth of it easily without squinting.');
  const para5 = translateVisibleText('The only connections this lake has are a small creek trickling in from the north, and a slow, shallow stream exiting it to the west.');
  const para6 = translateVisibleText('Certainly confusing, but you have more things to worry about now. Some of the ship you were on seems to have made it to this strange lakeside alongside you, but you see no evidence of other survivors. You spend the rest of the day collecting debris and searching wreckage. You manage to scrounge together some remnants of what was probably the sail, and set up a simple shelter for the night.');
  const para7 = translateVisibleText("The night, thankfully, passes quickly. As you make your way outside in the morning, you see small tracks left by some evening passerby, not far from your makeshift tent. Just the thought of something else alive makes you realize how hungry you are. Maybe you can find some animal to eat, or, if you're lucky, a tavern. You slide a small metal shard into your pocket to use as a knife, and break off an unrotted piece of wood as a primitive club.");
  const para8 = translateVisibleText("By midday, you are travelling through those beautiful golden stalks. This looks like farmland. Hopefully its farmer is nearby. You hear a rustling to your side, and turn to investigate. You'd hoped to find help, but your luck has betrayed you once again.");
  screen.innerHTML = `
    <div style="max-width:760px;margin:0 auto;">
      <div class="story-text">${para1}</div>
      <div class="story-text">${para2}</div>
      <div class="story-text">${para3}</div>
      <div class="story-text">${para4}</div>
      <div class="story-text">${para5}</div>
      <div class="story-text">${para6}</div>
      <div class="story-text">${para7}</div>
      <div class="story-text">${para8}</div>
      <div style="margin-top:30px;text-align:center;">
        <button class="btn primary" onclick="advanceFromLakeScene()">${translateVisibleText('Face What You Found')}</button>
      </div>
    </div>
  `;
  showScreen('story-screen');
}
