var questions = {
    easy: [
    {question: "What is the capital city of France?", answers: ["Paris", "London", "Madrid", "Rome"], correctAnswer: 0},
    {question: "Which planet is known as the Red Planet?", answers: ["Venus", "Mars", "Jupiter", "Saturn"], correctAnswer: 1},
    {question: "Who painted the Mona Lisa?", answers: ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"], correctAnswer: 0},
    {question: "Which animal is known as the 'King of the Jungle'?", answers: ["Lion", "Elephant", "Giraffe", "Tiger"], correctAnswer: 0},
    {question: "What is the largest organ in the human body?", answers: ["Liver", "Heart", "Skin", "Brain"], correctAnswer: 2},
    {question: "Which country is famous for the Great Wall?", answers: ["China", "India", "Brazil", "Australia"], correctAnswer: 0},
    {question: "Who wrote the play 'Romeo and Juliet'?", answers: ["William Shakespeare", "George Orwell", "J.R.R. Tolkien", "Jane Austen"], correctAnswer: 0},
    {question: "Which continent is the driest inhabited continent on Earth?", answers: ["Africa", "Asia", "Australia", "North America"], correctAnswer: 2},
    {question: "What is the chemical symbol for gold?", answers: ["Ag", "Au", "Fe", "Hg"], correctAnswer: 1},
    {question: "Which famous scientist developed the theory of relativity?", answers: ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Galileo Galilei"], correctAnswer: 1},
    {question: "Which sport is the most popular in the United States?", answers: ["Football", "Basketball", "Baseball", "Soccer"], correctAnswer: 0},
    {question: "Which city is known as the 'Big Apple'?", answers: ["Los Angeles", "Chicago", "New York City", "Miami"], correctAnswer: 2},
    {question: "What is the largest ocean in the world?", answers: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], correctAnswer: 3},
    {question: "Which famous artist painted the ceiling of the Sistine Chapel?", answers: ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"], correctAnswer: 3},
    {question: "Who was the first person to step foot on the moon?", answers: ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "John F. Kennedy"], correctAnswer: 0},
    {question: "Which country is famous for the Taj Mahal?", answers: ["India", "China", "Egypt", "Greece"], correctAnswer: 0},
    {question: "What is the largest continent in the world?", answers: ["Africa", "Asia", "Europe", "South America"], correctAnswer: 1},
    {question: "Who wrote the novel 'Pride and Prejudice'?", answers: ["Jane Austen", "Emily Bronte", "Charlotte Bronte", "Virginia Woolf"], correctAnswer: 0},
    {question: "What is the largest desert in the world?", answers: ["Gobi Desert", "Sahara Desert", "Atacama Desert", "Kalahari Desert"], correctAnswer: 1},
    {question: "Which instrument is known as the 'king of instruments'?", answers: ["Piano", "Guitar", "Violin", "Organ"], correctAnswer: 3},
    {question: "What is the largest species of shark?", answers: ["Great White Shark", "Hammerhead Shark", "Whale Shark", "Tiger Shark"], correctAnswer: 2},
    {question: "Who is the author of the Harry Potter book series?", answers: ["J.K. Rowling", "Stephen King", "George R.R. Martin", "Suzanne Collins"], correctAnswer: 0},
    {question: "Which country is famous for the Colosseum?", answers: ["Italy", "Greece", "Spain", "France"], correctAnswer: 0},
    {question: "What is the smallest planet in our solar system?", answers: ["Mercury", "Mars", "Venus", "Earth"], correctAnswer: 0},
    {question: "Who is the Greek god of the sea?", answers: ["Zeus", "Poseidon", "Hades", "Apollo"], correctAnswer: 1}
    ],
    medium: [
    {question: "Who painted the famous artwork 'The Starry Night'?", answers: ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"], correctAnswer: 1},
    {question: "What is the capital city of Australia?", answers: ["Sydney", "Melbourne", "Canberra", "Perth"], correctAnswer: 2},
    {question: "Which country is known as the 'Land of the Rising Sun'?", answers: ["China", "Japan", "Thailand", "South Korea"], correctAnswer: 1},
    {question: "What is the currency of Brazil?", answers: ["Peso", "Yen", "Real", "Euro"], correctAnswer: 2},
    {question: "Who wrote the novel 'To Kill a Mockingbird'?", answers: ["F. Scott Fitzgerald", "Harper Lee", "J.D. Salinger", "Mark Twain"], correctAnswer: 1},
    {question: "Which animal is the tallest in the world?", answers: ["Elephant", "Giraffe", "Horse", "Kangaroo"], correctAnswer: 1},
    {question: "What is the largest organ in the human body?", answers: ["Liver", "Heart", "Skin", "Brain"], correctAnswer: 2},
    {question: "Which country hosted the 2016 Summer Olympics?", answers: ["Brazil", "United States", "China", "Russia"], correctAnswer: 0},
    {question: "What is the chemical symbol for sodium?", answers: ["Na", "So", "K", "Mg"], correctAnswer: 0},
    {question: "Which famous scientist developed the theory of general relativity?", answers: ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Galileo Galilei"], correctAnswer: 1},
    {question: "Which city is famous for the Leaning Tower?", answers: ["Rome", "Venice", "Florence", "Pisa"], correctAnswer: 3},
    {question: "What is the largest ocean in the world?", answers: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], correctAnswer: 3},
    {question: "Who painted the ceiling of the Sistine Chapel?", answers: ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"], correctAnswer: 3},
    {question: "Who is the author of the novel '1984'?", answers: ["George Orwell", "Aldous Huxley", "Ray Bradbury", "J.R.R. Tolkien"], correctAnswer: 0},
    {question: "Which country is famous for the Great Barrier Reef?", answers: ["Australia", "Mexico", "Maldives", "Indonesia"], correctAnswer: 0},
    {question: "Which city is known as the 'Eternal City'?", answers: ["Athens", "Rome", "Istanbul", "Cairo"], correctAnswer: 1},
    {question: "What is the largest desert in the world?", answers: ["Gobi Desert", "Sahara Desert", "Atacama Desert", "Kalahari Desert"], correctAnswer: 1},
    {question: "Who wrote the play 'Hamlet'?", answers: ["William Shakespeare", "Arthur Miller", "Anton Chekhov", "Oscar Wilde"], correctAnswer: 0},
    {question: "What is the tallest mountain in the world?", answers: ["Mount Everest", "K2", "Kilimanjaro", "Mount Fuji"], correctAnswer: 0},
    {question: "Which instrument has black and white keys and is commonly found in classical music?", answers: ["Guitar", "Violin", "Piano", "Trumpet"], correctAnswer: 2},
    {question: "Who is the author of the novel 'The Great Gatsby'?", answers: ["F. Scott Fitzgerald", "Ernest Hemingway", "Jane Austen", "Virginia Woolf"], correctAnswer: 0},
    {question: "What is the largest country in South America?", answers: ["Argentina", "Brazil", "Colombia", "Peru"], correctAnswer: 1},
    {question: "Who is the main protagonist in J.R.R. Tolkien's 'The Lord of the Rings'?", answers: ["Frodo Baggins", "Gandalf", "Aragorn", "Bilbo Baggins"], correctAnswer: 0},
    {question: "Which country is famous for the Pyramids of Giza?", answers: ["Egypt", "Mexico", "Greece", "India"], correctAnswer: 0},
    {question: "What is the largest lake in Africa?", answers: ["Lake Victoria", "Lake Tanganyika", "Lake Malawi", "Lake Chad"], correctAnswer: 0}
    ],
    hard: [
    {question: "Which artist painted the famous artwork 'Guernica'?", answers: ["Pablo Picasso", "Salvador Dalí", "Vincent van Gogh", "Claude Monet"], correctAnswer: 0},
    {question: "What is the capital city of Canada?", answers: ["Toronto", "Vancouver", "Ottawa", "Montreal"], correctAnswer: 2},
    {question: "Which country is known as the 'Land of the Pharaohs'?", answers: ["Greece", "Egypt", "Morocco", "Turkey"], correctAnswer: 1},
    {question: "What is the currency of Japan?", answers: ["Yuan", "Yen", "Rupee", "Pound"], correctAnswer: 1},
    {question: "Who wrote the novel 'War and Peace'?", answers: ["Leo Tolstoy", "Fyodor Dostoevsky", "Anton Chekhov", "Mikhail Bulgakov"], correctAnswer: 0},
    {question: "Which animal has the longest lifespan?", answers: ["Elephant", "Giant Tortoise", "Bowhead Whale", "Blue Whale"], correctAnswer: 1},
    {question: "What is the largest internal organ in the human body?", answers: ["Liver", "Heart", "Kidney", "Lung"], correctAnswer: 0},
    {question: "Which country hosted the 2018 FIFA World Cup?", answers: ["Germany", "Brazil", "Russia", "France"], correctAnswer: 2},
    {question: "What is the chemical symbol for silver?", answers: ["Ag", "Si", "Sr", "Sn"], correctAnswer: 0},
    {question: "Who proposed the theory of general relativity?", answers: ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Galileo Galilei"], correctAnswer: 1},
    {question: "Which city is famous for the Acropolis?", answers: ["Athens", "Rome", "Cairo", "Istanbul"], correctAnswer: 0},
    {question: "What is the deepest point in the world's oceans?", answers: ["Mariana Trench", "Puerto Rico Trench", "Java Trench", "Tonga Trench"], correctAnswer: 0},
    {question: "Who painted the artwork 'The Persistence of Memory'?", answers: ["Salvador Dalí", "Pablo Picasso", "Vincent van Gogh", "Edvard Munch"], correctAnswer: 0},
    {question: "Who is the author of the novel 'One Hundred Years of Solitude'?", answers: ["Gabriel García Márquez", "Isabel Allende", "Jorge Luis Borges", "Mario Vargas Llosa"], correctAnswer: 0},
    {question: "Which country is famous for the Petra archaeological site?", answers: ["Israel", "Jordan", "Lebanon", "Egypt"], correctAnswer: 1},
    {question: "Which city is known as the 'City of Light'?", answers: ["Paris", "Rome", "Prague", "Barcelona"], correctAnswer: 0},
    {question: "What is the driest place on Earth?", answers: ["Atacama Desert", "Sahara Desert", "Death Valley", "McMurdo Dry Valleys"], correctAnswer: 3},
    {question: "Who wrote the play 'Macbeth'?", answers: ["William Shakespeare", "Anton Chekhov", "Henrik Ibsen", "Oscar Wilde"], correctAnswer: 0},
    {question: "Which mountain range is the highest in the world?", answers: ["Andes", "Himalayas", "Rocky Mountains", "Alps"], correctAnswer: 1},
    {question: "Which instrument has the highest pitch in an orchestra?", answers: ["Flute", "Piccolo", "Violin", "Trumpet"], correctAnswer: 1},
    {question: "Who is the author of the novel 'Ulysses'?", answers: ["James Joyce", "Virginia Woolf", "F. Scott Fitzgerald", "Ernest Hemingway"], correctAnswer: 0},
    {question: "Which country is famous for the Angkor Wat temple complex?", answers: ["Thailand", "Cambodia", "Vietnam", "Laos"], correctAnswer: 1},
    {question: "Who is the main antagonist in J.R.R. Tolkien's 'The Hobbit'?", answers: ["Smaug", "Gollum", "Saruman", "Azog"], correctAnswer: 0},
    {question: "What is the largest pyramid in Egypt?", answers: ["Pyramid of Khufu", "Pyramid of Khafre", "Pyramid of Menkaure", "Step Pyramid of Djoser"], correctAnswer: 0},
    {question: "What is the largest lake in North America?", answers: ["Lake Superior", "Lake Michigan", "Lake Ontario", "Lake Huron"], correctAnswer: 0}
    ]
};

var score = 0;
var currentQuestion = 0;
var currentDifficulty = '';
var difficultyPoints = {easy: 10, medium: 15, hard: 20};
var startSound = new Audio('../static/games/quiz/intro.mp3');
startSound.loop = false;
var questionSound = new Audio('../static/games/quiz/countdown.mp3');
startSound.loop = false;
var correctSound = new Audio('../static/games/quiz/correct.mp3');
startSound.loop = false;
var wrongSound = new Audio('../static/games/quiz/wrong.mp3');
startSound.loop = false;
var removeSound = new Audio('../static/games/quiz/remove.mp3');
startSound.loop = false;
var timeoutSound = new Audio('../static/games/quiz/timeout.mp3');


console.log("Declarations complete. Values are:", questions, score, currentQuestion, currentDifficulty, difficultyPoints);

// Lifelines
var lifelines = {
  fiftyFifty: {used: false},
  askAudience: {used: false},
  askGpt: {used: false},
  freezeTimer: {used: false},
};

var countdown;

$(document).ready(function() {
    // Play start sound
    startSound.play();

    $.ajax({
        url: '/api/get_highscores',
        method: 'GET',
        data: {game_name: 'Quiz Game'},
        success: function(highscores) {
            var table = $(".game-highscores");
            for (var i = 0; i < highscores.length; i++) {
                var row = $("<tr></tr>");
                row.append($("<td></td>").text(highscores[i].user_name));
                row.append($("<td></td>").text(highscores[i].highscore));
                table.append(row);
            }
        }
    });



    $(".difficulty").click(function() {
        // Reset lifelines and buttons
        lifelines = {
            fiftyFifty: {used: false},
            askAudience: {used: false},
            askGpt: {used: false},
            freezeTimer: {used: false},
        };
        $(".lifeline-btn").removeClass("used");

        // Stop the start sound
        startSound.pause();
        startSound.currentTime = 0;

        currentDifficulty = $(this).attr('id');
        $("#difficultySelection").hide();
        $("#quiz").show();
        $(".lifelines").show();
        showQuestion();
        startCountdown();
    });

    $(document).on("click", ".answer", function() {
        clearInterval(countdown);
        var selectedAnswerCorrect = $(this).data("correct");
        evaluateAnswer(selectedAnswerCorrect);
    });


    $(document).on("click", "#fiftyFifty", function() {
        if (!lifelines.fiftyFifty.used) {
            lifelines.fiftyFifty.used = true;
            removeIncorrectAnswers();
            $(this).addClass("used");
        }
    });

    $(document).on("click", "#askAudience", function() {
        if (!lifelines.askAudience.used) {
            lifelines.askAudience.used = true;
            showAudienceResponse();
            $(this).addClass("used");
        }
    });

    $(document).on("click", "#askGpt", function() {
        if (!lifelines.askGpt.used) {
            lifelines.askGpt.used = true;
            askGptForAnswer();
            $(this).addClass("used");
        }
    });

    $(document).on("click", "#freezeTimer", function() {
        if (!lifelines.freezeTimer.used) {
            lifelines.freezeTimer.used = true;
            freezeCountdown();
            $(this).addClass("used");
        }
    });
});

function startCountdown() {
  var timer = 10;
  $("#timer").text("Timer: " + timer);

  countdown = setInterval(function() {
    timer--;
    $("#timer").text("Timer: " + timer);

    if (timer <= 0) {
      clearInterval(countdown);
      evaluateAnswer(false, "TIMEOUT"); // Always treat timeout as incorrect
    }
  }, 1000);
}

function freezeCountdown() {
  clearInterval(countdown);
}



function removeIncorrectAnswers() {
  var currentQuestionObject = questions[currentDifficulty][currentQuestion];

  var incorrectIndices = [];
  for (var i = 0; i < currentQuestionObject.answers.length; i++) {
    if (i !== currentQuestionObject.correctAnswer) {
      incorrectIndices.push(i);
    }
  }

  // Only proceed if we have at least two incorrect answers
  if (incorrectIndices.length >= 2) {
    // Randomly select two incorrect answers to remove
    var indicesToRemove = _.sampleSize(incorrectIndices, 2);

    // Play remove sound
    removeSound.play();

    // Remove the buttons and make it visually appealing
    for (var i = 0; i < indicesToRemove.length; i++) {
      $("#answer" + indicesToRemove[i])
        .fadeOut(500, function() { $(this).remove(); });
    }
  }
}



function showAudienceResponse() {
  var currentQuestionObject = questions[currentDifficulty][currentQuestion];

  var remainingPercentage = 100;
  var audiencePercentages = [];

  // Create random percentages for each incorrect answer
  for (var i = 0; i < currentQuestionObject.answers.length - 1; i++) {
    var maxPercentage = remainingPercentage - (currentQuestionObject.answers.length - i - 1);
    var thisPercentage = Math.floor(Math.random() * (maxPercentage + 1));
    audiencePercentages.push(thisPercentage);
    remainingPercentage -= thisPercentage;
  }

  // Assign the remaining percentage to the last answer
  audiencePercentages.push(remainingPercentage);

  // Sort the percentages and ensure the highest one is on the correct answer 75% of the time
  audiencePercentages.sort(function(a, b) { return a - b; });
  if (Math.random() > 0.25) {
    var correctPercentage = audiencePercentages.pop();
    audiencePercentages.splice(currentQuestionObject.correctAnswer, 0, correctPercentage);
  }

  // Display the percentages
  for (var i = 0; i < audiencePercentages.length; i++) {
    var answerPercentage = $("<span></span>")
      .addClass("answerPercentage")
      .text(audiencePercentages[i] + "%");
    $("#answer" + i).after(answerPercentage);
  }
}


function askGptForAnswer() {
  var currentQuestionObject = questions[currentDifficulty][currentQuestion];

  var percentagePerAnswer = [];
  var remainingPercentage = 100;
  var wrongIndices = [];

  // Calculate random percentages for each answer
  for (var i = 0; i < currentQuestionObject.answers.length - 1; i++) {
    var randomPercentage = Math.floor(Math.random() * remainingPercentage);
    percentagePerAnswer[i] = randomPercentage;
    remainingPercentage -= randomPercentage;

    if (i !== currentQuestionObject.correctAnswer) {
      wrongIndices.push(i);
    }
  }
  // Assign the remaining percentage to the last answer
  percentagePerAnswer[currentQuestionObject.answers.length - 1] = remainingPercentage;

  var highestPercentageIndex;
  // 85% chance the highest percentage will be for the correct answer
  if (Math.random() < 0.85) {
    highestPercentageIndex = currentQuestionObject.correctAnswer;
  }
  // 15% chance the highest percentage will be for a wrong answer
  else {
    highestPercentageIndex = _.sample(wrongIndices);
  }

  // Swap the highest percentage to its new index
  var highestPercentage = Math.max(...percentagePerAnswer);
  var highestPercentageOldIndex = percentagePerAnswer.indexOf(highestPercentage);
  var temp = percentagePerAnswer[highestPercentageIndex];
  percentagePerAnswer[highestPercentageIndex] = highestPercentage;
  percentagePerAnswer[highestPercentageOldIndex] = temp;

  // Display the percentages
  for (var i = 0; i < percentagePerAnswer.length; i++) {
    var answerPercentage = $("<span></span>")
      .addClass("answerPercentage")
      .text(percentagePerAnswer[i] + "%");
    $("#answer" + i).after(answerPercentage);
  }
}


function evaluateAnswer(selectedAnswerCorrect, reason = "") {
  var feedbackMessage;
  var feedbackColor;
  var feedbackClass;
  var soundToPlay;

  // Added special handling for TIMEOUT
  if (reason === "TIMEOUT") {
    score -= 2; // You lose 2 points
    feedbackMessage = "Timeout!";
    feedbackClass = "incorrect";
    feedbackColor = "red";
    soundToPlay = timeoutSound; // Play timeout sound
  }
  else if (selectedAnswerCorrect) {
    score += difficultyPoints[currentDifficulty];
    feedbackMessage = "Correct!";
    feedbackClass = "correct";
    feedbackColor = "green";
    soundToPlay = correctSound;
  } else {
    feedbackMessage = "Wrong!";
    feedbackClass = "incorrect";
    feedbackColor = "red";
    soundToPlay = wrongSound;
  }

  // Play sound
  soundToPlay.play();

  $(".answerPercentage").remove();

  currentQuestion++;
  $("#scoreValue").text("Current Score: " + score);

  var pauseAndShowNextQuestion = function() {
    if (currentQuestion < questions[currentDifficulty].length) {
      showQuestion();
      startCountdown();
    } else {
      $("#quiz").hide();
      $("#finalScore").text("Final Score: " + score);
      $("#score").show();
      submitScore();
    }
  };

  // Pause for 2 seconds on timeout before showing the next question
  if (reason === "TIMEOUT") {
    setTimeout(pauseAndShowNextQuestion, 2000);
  } else {
    pauseAndShowNextQuestion();
  }

  // Display feedback message
  var flashMessage = $("<li></li>")
    .text(feedbackMessage)
    .addClass(feedbackClass)
    .css("color", feedbackColor)
    .hide()
    .fadeIn(200)
    .fadeOut(200)
    .fadeIn(200)
    .fadeOut(200);
  $(".flash-messages").append(flashMessage);
}


function showQuestion() {
    var questionObject = questions[currentDifficulty][currentQuestion];
    $("#question").text(questionObject.question);

    // Clear existing answer buttons
    $(".answer").remove();

    // Create answer buttons
    for (var i = 0; i < questionObject.answers.length; i++) {
        var answerButton = $("<button></button>")
            .addClass("answer")
            .attr("id", "answer" + i)
            .attr("data-correct", i === questionObject.correctAnswer)
            .text(questionObject.answers[i]);
        $("#answers").append(answerButton);
    }

}


function submitScore() {
    var requestUrl = '/api/save_highscore';
    var requestData = JSON.stringify({game_name: 'Quiz Game', highscore: score});
    var requestHeaders = {'X-Auth-Token': token};

    $.ajax({
        url: requestUrl,
        method: 'POST',
        headers: requestHeaders,
        data: requestData,
        contentType: 'application/json',
        success: function() {
            $("#submissionStatus").text("Score submitted successfully!");
        },
        error: function() {
            $("#submissionStatus").text("Failed to submit score.");
        }
    });


}
