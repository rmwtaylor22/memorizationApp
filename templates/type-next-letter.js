/*
 * @file type-next-letter.js
 * @author Stefan Brandle
 * @date Tue Apr  2 14:05:21 EDT 2019
 *
 */
"use strict";

startReviewButton.addEventListener("click", startReview);
startActivityButton.addEventListener("click", startActivity);
startActivityButton.addEventListener("click", stopReview);
quitActivityButton.addEventListener("click", quitActivity);

var verseObj = {
    ref:"John 3:16",
    wordCount:0,
    words:[],
	//hiddenWords:[],
	guessableWordsIndex:[],
	text:"For God so loved the world that he gave his one and only Son,\
		  that whoever believes in him shall not perish but have eternal life.",
    showTimer:true,
	difficultyLevel:1
};

const enterKeyCode = 13;
var nextIndex = null;
var guessesLeft = 3;
var score = 0;
var errorCount = 0;
var timerId = null;
var clockTime = 0;
var activityStartTime;
var activityStopTime;
var reviewStartTime;
var reviewStopTime;
var passStartTime;
var perfect = true;

// This is set later after the verse has been parsed.
var hiddenWordDelta = null;

// numWordsToGuess is incremented by hiddenWordDelta every time raise challenge level.
var numWordsToGuess = 0;

function createWordArray(text) {
	var words = [];
    var tmp = text.split(/\s*\b\s*/);
	var tempObj = null;

	for(var i=0; i<tmp.length; i++) {
		tempObj = {item:tmp[i], guessable:true, isWord:true};
		if(/^[a-zA-Z]+$/.test(tmp[i])) {
			verseObj.wordCount++;
			verseObj.guessableWordsIndex.push(i);
		} else {
			tempObj.guessable = false;
			tempObj.isWord = false;
		}
		// Nothing originally marked as hidden
		tempObj.isHidden = false;
		words.push(tempObj);
	}
	return words;
}

function randomizeIndexOrder(wordIndex) {
	var len = wordIndex.length;

	for(var i=0; i<wordIndex.length; i++) {
		var swapIndex = Math.trunc(Math.random()*len);
        var tmp = wordIndex[swapIndex];
		wordIndex[swapIndex] = wordIndex[i];
		wordIndex[i] = tmp;
	}
    return wordIndex;
}

function startReview(event) {
	verseObj.words = createWordArray(verseObj.text);
	hiddenWordDelta = Math.ceil(verseObj.wordCount/5);
	reviewStartTime = new Date().getTime();

	refSpan.innerHTML = verseObj.ref;
	textSpan.innerHTML = verseObj.text;
    reviewDiv.classList.remove("hidden");

	startReviewButton.setAttribute("disabled", true);
	startActivityButton.removeAttribute("disabled");
	quitActivityButton.removeAttribute("disabled");
}

function startActivity(/*event*/) {
	// Log start
	var d = new Date()
	activityStartTime = d.getTime();

	//------------------------------------------
	// Identify which words are to be hidden
	//------------------------------------------
	// Create index of words in random order. First numWordsToGuess words will be hidden.
	verseObj.guessableWordsIndex = randomizeIndexOrder(verseObj.guessableWordsIndex);

	// Bump up the number of words to be hidden. NOTE: first time through, don't depend on perfect.
	// After that, increase number of words to guess only if no errors previous time.
	if((numWordsToGuess==0||perfect) && numWordsToGuess<verseObj.wordCount) {
		numWordsToGuess += hiddenWordDelta;
		if(numWordsToGuess>verseObj.wordCount) {
			// Cannot guess more words than there are
			numWordsToGuess = verseObj.wordCount;
		}
	}
	wordCountSpan.innerHTML = numWordsToGuess;

	// Reset isHidden attribute of all words
	for (var i=0; i<verseObj.words.length; i++) {
		verseObj.words[i].isHidden = false;
	}

	// Mark the words to be hidden
	for(var i=0; i<numWordsToGuess; i++){
		// Mark the first numWordsToGuess to be hidden using guessableWordsIndex
		verseObj.words[verseObj.guessableWordsIndex[i]].isHidden = true;
	}

	// Reset variables and display values
	score = 0;
	clockTime = 0;
	perfect = false;

	reviewDiv.classList.add("hidden");
	activity.classList.remove("hidden");
	startActivityButton.setAttribute("disabled", true);
	quitActivityButton.removeAttribute("disabled");

	if(verseObj.showTimer == false) {
		clockField.classList.add("hidden");
	}
	// Clear the current contents of the div that holds the words
	wordDiv.innerHTML = "";

	guessesLeftSpan.innerHTML = 3;
	errorCountSpan.innerHTML = 0;
	scoreSpan.innerHTML = 0;
	clockSpan.innerHTML = 0;

	for (var i=0; i<verseObj.words.length; i++) {
		var outerSpan = document.createElement("span");
		var span = document.createElement("span");
		span.innerHTML = verseObj.words[i].item;
		span.id = "span"+i;
		outerSpan.appendChild(span);
		wordDiv.appendChild(outerSpan);
		span.classList.add("verseItemSpan");
		if(verseObj.words[i].isHidden==true) {
			span.classList.add("notGuessed");
		} else {
			// gets displayed: no CSS class
		}
	}

	// Find the first word that is hidden
	nextIndex = getNextGuessableWordIndex(-1, verseObj);
	
	var nextSpan = document.getElementById("span"+nextIndex);
	if(nextSpan) {
		console.log("Next word to be guessed:", nextSpan.innerHTML);
		nextSpan.parentElement.classList.add("selectedWord");
	} else {
		console.log("startActivity(): nextSpan invalid");
	}

	document.addEventListener("keyup", handleGuess);
    topRow.classList.remove("hidden");
	timerId = setInterval(incrementClock, 1000);
}

function stopReview(/*event*/) {
	startActivityButton.removeEventListener("click", stopReview);
	var d = new Date()
    reviewStopTime = d.getTime();
}

function quitActivity(/*event*/) {
	var d = new Date()
	activityStopTime = d.getTime();

	startActivityButton.setAttribute("disabled", true);
	startActivityButton.setAttribute("value", "Memorize");

	startReviewButton.removeAttribute("disabled");
	quitActivityButton.setAttribute("disabled", true);
	clearInterval(timerId);
	document.removeEventListener("keyup", handleGuess);
    //wordDiv.innerHTML = "";
	reviewDiv.classList.add("hidden");
	activity.classList.add("hidden");
	topRow.classList.add("hidden");
}

function incrementClock(){
	clockTime++;
	clockSpan.innerHTML = clockTime;
}

function handleGuess(event){
	console.assert(nextIndex!==null, "nextIndex is null: should have been set to something");

	if(nextIndex == -1) {
		// Making it so user doesn't have to click "memorize", but can just press <Enter>
		if(event.keyCode==enterKeyCode) {
			/*
			 * TODO: if perfect AND guessed all words, ENTER => quit
			if(perfect) {
				quitActivity();
			} else {
			*/
			startActivity();
		}
		return;
	}

	if (nextIndex>=verseObj.words.length) {
		return;
	}

	var span = document.getElementById("span"+nextIndex);
	console.assert(span, "span"+nextIndex+ " was invalid");
	// Return if span is invalid. Keyboard event after completed memorization pass.
	if( !span ) return;

	if (span.innerHTML[0].toUpperCase() == event.key.toUpperCase()) {
		// Guessed correctly
		//console.log("guessed correctly");
		span.classList.add("correctlyGuessed");
		score += guessesLeft / 3;
		if(guessesLeftSpan.classList.contains("guesses2")) {
			guessesLeftSpan.classList.remove("guesses2");
		}
		if(guessesLeftSpan.classList.contains("guesses1")) {
			guessesLeftSpan.classList.remove("guesses1");
		}
		guessesLeftSpan.classList.add("guesses3");
		scoreSpan.innerHTML = score.toFixed(1);
		percentCorrectSpan.innerHTML = (100*score/numWordsToGuess).toFixed(1)+"%";

		span.parentElement.classList.remove("selectedWord");

		// Correct. Unmark the current word and move to next.
		nextIndex = getNextGuessableWordIndex(nextIndex, verseObj);
		var nextSpan = document.getElementById("span"+nextIndex);
		if(nextSpan) {
			nextSpan.parentElement.classList.add("selectedWord");
		}
		

		guessesLeft = 3;
	} else if(/^[A-Za-z]$/.test(event.key)) {
		// Guessed incorrectly: valid character
		//console.log("guessed incorrectly");
		guessesLeft--;
		if(guessesLeft==2) {
			guessesLeftSpan.classList.remove("guesses3");
			span.classList.remove("guesses3");
			guessesLeftSpan.classList.add("guesses2");
			span.classList.add("guesses2");
		} else if(guessesLeft==1) {
			guessesLeftSpan.classList.remove("guesses2");
			span.classList.remove("guesses2");
			guessesLeftSpan.classList.add("guesses1");
			span.classList.add("guesses1");
		} else if(guessesLeft==0) {
			guessesLeftSpan.classList.remove("guesses1");
			span.classList.remove("guesses1");
			guessesLeftSpan.classList.add("guesses0");
		}
		//console.log(event.key, "does not match");	
	} else {
		// Guessed incorrectly: invalid character => ignore
		//console.log("ignoring", event.key);	
	}

	if( guessesLeft<=0 ) {
		// Ran out of guesses
		span.classList.add("incorrectlyGuessed");
		guessesLeftSpan.classList.remove("guesses0");
		guessesLeftSpan.classList.add("guesses3");

		// Correct. Unmark the current word
		span.parentElement.classList.remove("selectedWord");
		
		nextIndex = getNextGuessableWordIndex(nextIndex, verseObj);

		// Correct. mark the next word
		var nextSpan = document.getElementById("span"+nextIndex);
		if(nextSpan) {
			nextSpan.parentElement.classList.add("selectedWord");
		}

		guessesLeft = 3;
		errorCount++;
		errorCountSpan.innerHTML = errorCount;
	}
	guessesLeftSpan.innerHTML = guessesLeft;

	if( nextIndex==-1 ) {
		// Reset nextIndex so ready for the next pass over verse.
		clearInterval(timerId);
	
		activityStopTime = new Date().getTime();

		startActivityButton.removeAttribute("disabled");
		startActivityButton.setAttribute("value", "Next");
		//quitActivityButton.setAttribute("disabled", true);

		perfect = score==numWordsToGuess;

		var logSummary = {};
		//logSummary.wordsCorrect = 
		logSummary.percentCorrect = (100*score/numWordsToGuess).toFixed(1);
		logSummary.clockTime = clockTime;
		logSummary.perfect = score==numWordsToGuess;
		logSummary.reviewStartTime = reviewStartTime;
		logSummary.reviewStopTime = reviewStopTime;
		logSummary.activityStartTime = reviewStartTime;
		logSummary.activityStopTime = activityStopTime;
		logSummary.reviewSeconds = Math.ceil((reviewStopTime-reviewStartTime)/1000);
		logSummary.activitySeconds = Math.ceil((activityStopTime-activityStartTime)/1000);
        doExternalUpdates(logSummary);
	} 
}

function getNextGuessableWordIndex(nextIndex, verseObj) {
	if(nextIndex===null || nextIndex==-1) {
		// Apparently just starting up
		nextIndex = 0;
	} else {
		// Move past the previous word
		nextIndex++;
	}

	while(nextIndex<verseObj.words.length && verseObj.words[nextIndex].isHidden==false) {
		// Finding next word to guess
		nextIndex++;
	}

	if(nextIndex>=verseObj.words.length) {
		// Ran off end of words
		nextIndex = -1;
	}
	return nextIndex;
}

function doExternalUpdates(dict){
    for(var key in dict) {
		console.log("doUpdate:",key,"=",dict[key]);
	}
}

