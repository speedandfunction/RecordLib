# RecordLib

Library for handling Criminal Records information in Pennsylvania.

Right now this is only an experimental project for trying out some ideas and new tooling (e.g., trying out some of the newer python features like type annotations and data classes)




## Goals

The ultimate goal is to develop a flexible and transparent pipeline for analyzing criminal records in Pennsylvania for expungeable and sealable cases and charges. We'd like to be able to take various inputs - pdf dockets, web forms, scanned summary sheets - build an idea of what a person's criminal record looks like, and then produce an analysis of what can be expunged or sealed (and _why_ we think different things can be expunged or sealed).


The pieces of this pipeline could be used in different interfaces.

A commandline tool could process a list of documents or the names of clients, and try to analyze the whole list in bulk.

A web application could take a user through the steps of the pipeline and allow the user to see how the analysis proceeds from inputs to output petitions. The application could allow the user to load some documents, then manually check the Record that the system builds out of those documents before proceeding to analyze the record.

Ideally, the expungement rules that get applied will also be written in a clear enough way that non-programmer lawyers can review them.

## Domain Model

There are five kinds of objects involved in this framework.


1. Criminal Records raw inputs - these are things like a pdf of a docket or a web form that asks a user about criminal record information.
2. A Criminal Record - the authoritative representation of what a person's criminal record is. Its made by compiling raw inputs.
3. Expungement/Sealing Rules - functions that take a Record and return an analysis of how a specific expungement or sealing rule applies to the record. What charges or cases does a specific rule allow to be sealed/expunged?
4. Analysis - An object that encapsulates how different rules apply to a record
5. Document Generator - a function that takes an analysis and information about a user (i.e., their attorney identification info) and produces a set of documents that includes drafts of petitions for a court.


## Command line utilties

Find out how to use Recordlib from the [command line](/docs/pages/cli.rst)


## Developing

See installation for development [instructions](/docs/pages/developing.rst)

#### Testing

Read about testing [here](/docs/pages/testing.rst)


## Roadmap

Right now I'm working on several pieces more or less simultaneously.

1. grammars for parsing summary sheets and dockets from pdfs
2. The CRecord class for managing information about a person's record (what methods and properties does it need to have?)
3. RuleDef functions - functions that take a CRecord and apply a single legal rule to it. I'm trying to figure out the right thing to return.


## Developing Grammars

The project currently uses `parsimonious` and Parsing Expression Grammars to parse pdf documents and transform them from a pdf file to an xml document.

Developing grammars is pretty laborious. Some tips:

**Parse text w/ subrule** With parsimonious, you can try parsing a bit of text with a specific rule, with `mygrammar['rule'].parse("text")`

So if you have a variable of the lines of your document, then you can more quickly test specific parts of the doc with specific parts of the grammar.

**Autogenerate the NodeVisitor** RecordLib with Parsimonious transforms a document with a grammar in two phases. First, Parsimonious uses a grammar to build a tree of the document. Then a NodeVisitor visits each node of the tree and does something, using a NodeVisitor subclass we have to create. The `CustomVisitorFactory` from RecordLib creates such a NodeVisitor with default behavior that's helpful to us. By passing the Factory a list of the terminal and nonterminal symbols in the grammar, the Factory will give us a class that will take a parsed document and wrap everything under terminal and nonterminal symbols in tags with the symbol's name. Terminal symbols will also have their text contents included as the tag content. NonTerminal symbols will only wrap their children (who are eventually terminal symbols).

## other issues

**Text from PDFs**
Right now pdf-to-text parsing is done with pdftotext. I think it works really well, but relying on a binary like that does limit options for how to deploy a project like this (i.e, couldn't use heroku, I think). It also requires writing a file temporarily to disk, which is kind of yucky. The best-known python pdf parser, PyPDF2, appears not be maintained anymore.

**Handing uncertainty**
Its important that an Analysis be able to say that how a rule applies to a case or charge is uncertain. For example, if the grade is missing from a charge, the answer to expungement questions isn't True or False, its "we don't know because ..."  

## Additional Notes

Statutes contain a lot of section symbols: §. To make this symbol using vim or vim inspired keybindings, use CTL-K SE. That's Control K, then the uppercase letters S and E.