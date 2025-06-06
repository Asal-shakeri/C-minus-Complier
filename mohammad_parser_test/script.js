const firstFollow = require('first-follow');
const fs = require('fs');

const path = require('path');

function parseGrammarFile(filePath) {
    const raw = fs.readFileSync(filePath, 'utf8');

    const lines = raw
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0); // skip empty lines

    const rules = [];

    for (const line of lines) {
        const [left, rightSide] = line.split('⟶'); // Unicode arrow
        if (!left || !rightSide) {
            console.warn(`Skipping malformed line: ${line}`);
            continue;
        }

        const leftTrimmed = left.trim();
        const rightSymbols = rightSide.trim().split(/\s+/).map(sym => sym === 'ε' ? null : sym);

        rules.push({
            left: leftTrimmed,
            right: rightSymbols
        });
    }

    return rules;
}



['first.txt', 'follow.txt', 'predict.txt'].forEach(file => {
    fs.unlink(file, (err) => {
        if (err) {
            console.error('Could not delete the file. Maybe it never existed, like your hopes.');
            return;
        }
        console.log('File deleted. Sweet, sweet minimalism achieved.');
    });
}
);
// const rules = [
//     // S -> a b A
//     {
//         left: 'S',
//         right: ['a', 'b', 'A']
//     },

//     // A -> b c
//     {
//         left: 'A',
//         right: ['b', 'c']
//     },

//     // A -> ε
//     {
//         left: 'A',
//         right: [null]
//     }
// ];
const rules = parseGrammarFile(path.join(__dirname, 'grammar.txt'));
console.log("rules are : ",rules);

const { firstSets, followSets, predictSets } = firstFollow(rules);

console.log("first sets are : ");
for (const key in firstSets) {
  firstSets[key] = firstSets[key].map(symbol => symbol === null ? 'ε' : symbol);
}
 console.log(firstSets);

for (const [key, value] of Object.entries(firstSets)) {
    fs.appendFile('first.txt', `${key} ${value.join(' ')}\n`, (err) => {
        if (err) throw err;
        console.log('Data appended. Legacy extended.');
    });
}
/*
 *  // S: a
 *  // A: b, ε
 *
 *  {
 *    S: ['a'],
 *    A: ['b', null]
 *  }
 */
for (const key in followSets) {
  followSets[key] = followSets[key].map(symbol => symbol === '\x00' ? '$' : symbol);
}
console.log("follow sets are : ");
for (const [key, value] of Object.entries(followSets)) {
    fs.appendFile('follow.txt', `${key} ${value.join(' ')}\n`, (err) => {
        if (err) throw err;
        console.log('Data appended. Legacy extended.');
    });
}
console.log(followSets);
/*
 *  // S: ┤
 *  // A: ┤
 *
 *  {
 *    S: ['\u0000'],
 *    A: ['\u0000']
 *  }
 */

console.log("predict sets are : ");
for (const key in predictSets) {
  predictSets[key] = predictSets[key].map(symbol => symbol === '\x00' ? '$' : symbol);
}
console.log(predictSets);

for (const [key, value] of Object.entries(predictSets)) {
    fs.appendFile('predict.txt', `${key} ${value.join(' ')}\n`, (err) => {
        if (err) throw err;
        console.log('Data appended. Legacy extended.');
    });
}
/*
 *  // 1: a
 *  // 2: b
 *  // 3: ┤
 * 
 *  {
 *    '1': ['a'],
 *    '2': ['b'],
 *    '3': ['\u0000']
 *  }
*/