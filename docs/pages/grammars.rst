*****************************
Parsing dockets with grammars
*****************************

A `context-free grammar <https://en.wikipedia.org/wiki/Context-free_grammar>` is a tool for describing 
the possible content that a text might have. 

CFGs are also used to build parsers that transform raw text into a structured tree.

We use context free grammars to describe the content of dockets and summary sheets, and to transform
the raw docket and summary text into objects that represent court cases, charges, sentences, and so on. 

Developing Grammars
===================

The project currently uses `parsimonious` and Parsing Expression Grammars to parse pdf documents and transform them from a pdf file to an xml document.

Developing grammars is pretty laborious. Some tips:

**Parse text w/ subrule** With parsimonious, you can try parsing a bit of text with a specific rule, with `mygrammar['rule'].parse("text")`

So if you have a variable of the lines of your document, then you can more quickly test specific parts of the doc with specific parts of the grammar.

**Autogenerate the NodeVisitor** RecordLib with Parsimonious transforms a document with a grammar in two phases. First, Parsimonious uses a grammar to build a tree of the document. Then a NodeVisitor visits each node of the tree and does something, using a NodeVisitor subclass we have to create. The `CustomVisitorFactory` from RecordLib creates such a NodeVisitor with default behavior that's helpful to us. By passing the Factory a list of the terminal and nonterminal symbols in the grammar, the Factory will give us a class that will take a parsed document and wrap everything under terminal and nonterminal symbols in tags with the symbol's name. Terminal symbols will also have their text contents included as the tag content. NonTerminal symbols will only wrap their children (who are eventually terminal symbols).

