// Quick script to fix the escape sequences in loaded_bones.html
// Run this in the browser console to fix the text

const fixes = [
  { line: 2853, find: "You\\'ve", replace: "You've" },
  { line: 2853, find: "weren\\'t", replace: "weren't" },
  { line: 2853, find: "you\\'d", replace: "you'd" },
  { line: 2854, find: "they\\'re", replace: "they're" },
  { line: 2854, find: "you\\'ve", replace: "you've" },
  { line: 2916, find: "you\\'re", replace: "you're" },
  { line: 2917, find: "what\\'s", replace: "what's" },
  { line: 2973, find: "you\\'re", replace: "you're" },
  { line: 2973, find: "you\\'re", replace: "you're" },
  { line: 2974, find: "You\\'d", replace: "You'd" }
];

console.log("Replace these lines with properly quoted strings");
