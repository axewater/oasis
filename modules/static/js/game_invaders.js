const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    }
};

const game = new Phaser.Game(config);
function preload() {
    this.load.image('player', 'path/to/player.png');
    this.load.image('alien', 'path/to/alien.png');
    this.load.image('bullet', 'path/to/bullet.png');
}
let player;
let aliens;
let bullets;
let cursors;
let score = 0;
let scoreText;

function create() {
    // Player
    player = this.physics.add.sprite(config.width / 2, config.height - 50, 'player');
    player.setCollideWorldBounds(true);

    // Aliens
    aliens = this.physics.add.group({ key: 'alien', repeat: 49, setXY: { x: 12, y: 0, stepX: 70, stepY: 50 } });

    // Bullets
    bullets = this.physics.add.group();

    // Input
    cursors = this.input.keyboard.createCursorKeys();
    this.input.keyboard.on('keydown_SPACE', shootBullet, this);

    // Score
    scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#FFF' });
    // Inside the create function:
    this.tweens.add({
        targets: aliens.getChildren(),
        x: '+=200',
        ease: 'Linear',
        duration: 2000,
        yoyo: true,
        repeat: -1
    });

    // Function to make aliens shoot
    function alienShoot() {
        const alien = Phaser.Utils.Array.GetRandom(aliens.getChildren());
        if (alien) {
            const alienBullet = bullets.create(alien.x, alien.y, 'bullet');
            alienBullet.setVelocityY(200);
        }
    }

    // Set aliens to shoot periodically
    this.time.addEvent({ delay: 2000, callback: alienShoot, callbackScope: this, loop: true });

    // Collision between player bullets and aliens
    this.physics.add.collider(bullets, aliens, hitAlien, null, this);

    // Collision between alien bullets and barriers or other objects here

    // Hit Alien function
    function hitAlien(bullet, alien) {
        bullet.destroy();
        alien.destroy();
        score += 10;
        scoreText.setText('Score: ' + score);
    }

}
function update() {
    // Player movement
    if (cursors.left.isDown) player.setVelocityX(-200);
    else if (cursors.right.isDown) player.setVelocityX(200);
    else player.setVelocityX(0);

    // Bullet movement
    bullets.children.iterate(function (bullet) {
        if (bullet) {
            if (bullet.y < 0) bullet.destroy();
        }
    });

    // Alien movement, collision, and increasing difficulty logic here
    if (score >= 100) {
    this.tweens.killTweensOf(aliens.getChildren());
    this.tweens.add({
        targets: aliens.getChildren(),
        x: '+=200',
        ease: 'Linear',
        duration: 1500, // Faster
        yoyo: true,
        repeat: -1
    });
    // Inside the update function, you can check for game over or victory conditions
    if (aliens.countActive(true) === 0) {
        scoreText.setText('Victory! Score: ' + score);
        // Optionally, you could transition to a victory scene here
    }

    if (gameOverCondition) { // Define this based on your game's logic
        scoreText.setText('Game Over! Score: ' + score);
        // Optionally, you could transition to a game over scene here
    }

}
}
function shootBullet() {
    const bullet = bullets.create(player.x, player.y, 'bullet');
    bullet.setVelocityY(-400);
}
