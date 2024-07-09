const crypto = require('crypto');
const readline = require('readline');

function help() {
    console.log(`
        Welcome to the Generalized Rock-Paper-Scissors game!

        Here are the rules:

        * You can choose a move by its index (number) or its name.
        * Available moves are displayed at the beginning of the game.
        * 0 - Exit the game
        * ? - Print this help message

        **Game Rules:**

        * Each move competes against half of the following moves in a circular order.
        * The goal is to choose a move that beats the computer's move.
        * If you choose the same move as the computer, it's a tie!

        Move Outcomes Table:

             |  Rock   |  Paper  | Scissors |  Lizard |  Spock
        --------------------------------------------------------
        Rock |   Tie   |  Lose   |   Win    |   Win   |  Lose
        Paper|   Win   |   Tie   |   Lose   |   Lose  |  Win
        Scissors| Lose  |   Win   |   Tie    |   Win   |  Lose
        Lizard|  Lose  |   Win   |   Lose   |   Tie   |  Win
        Spock |  Win   |   Lose  |   Win    |   Lose  |  Tie

        Good luck!
    `);
    process.exit(0);
}

function exit() {
    process.exit(0);
}

function generateSecretKey() {
    const secretKey = crypto.randomBytes(32).toString('hex');
    return secretKey;
}

function computeHmac(secretKey, choice) {
    const hmac = crypto.createHmac('sha256', Buffer.from(secretKey, 'hex'));
    hmac.update(choice);
    return hmac.digest('hex');
}

function availableMoves(moves) {
    console.log("Available moves:");
    moves.forEach((move, index) => {
        console.log(`${index + 1} - ${move}`);
    });
    console.log("0 - Exit");
    console.log("? - Help");
}

function computerMove(moves) {
    const randomIndex = Math.floor(Math.random() * moves.length);
    return moves[randomIndex];
}

async function userMove(moves) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    while (true) {
        const userChoice = await new Promise(resolve => {
            rl.question('Enter your move: ', resolve);
        });

        if (userChoice === '?') {
            help();
        } else if (!isNaN(userChoice)) {
            const choiceIndex = parseInt(userChoice, 10);
            if (choiceIndex === 0) {
                console.log("Exiting the game...");
                exit();
            } else if (choiceIndex >= 1 && choiceIndex <= moves.length) {
                rl.close();
                return moves[choiceIndex - 1];
            }
        } else if (moves.includes(userChoice)) {
            rl.close();
            return userChoice;
        }

        console.log("Invalid input. Please choose from available options.");
    }
}

function determineWinner(userMove, computerMove, moves) {
    const indexUser = moves.indexOf(userMove);
    const indexComputer = moves.indexOf(computerMove);
    const difference = (indexUser - indexComputer + moves.length) % moves.length;

    if (indexUser === indexComputer) {
        console.log("It's a tie!");
    } else if (difference === Math.floor(moves.length / 2)) {
        console.log("You Win! 🏆🥇");
    } else {
        console.log("You loose 😒");
    }
}

function main() {
    let moves = process.argv.slice(2);
    moves = [...new Set(moves)]
    if (moves.length < 3 || moves.length % 2 === 0) {
        console.log("Invalid number of moves provided.");
        console.log("Please provide an odd number of moves (≥ 3) as command line arguments.");
        console.log("Example: node script.js rock paper scissors lizard spock");
        process.exit(1);
    }

    const secretKey = generateSecretKey();

    const computerMoveChoice = computerMove(moves);
    const computerHmac = computeHmac(secretKey, computerMoveChoice);
    console.log(`Computer's HMAC: ${computerHmac}`);

    availableMoves(moves);
    userMove(moves).then(userMoveChoice => {
        console.log(`Your Move: ${userMoveChoice}`);
        console.log(`Computer Move: ${computerMoveChoice}`);

        determineWinner(userMoveChoice, computerMoveChoice, moves);
        console.log(`Secret Key: ${secretKey}`);
    });
}

if (require.main === module) {
    main();
}
