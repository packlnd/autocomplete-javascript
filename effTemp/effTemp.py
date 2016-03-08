import sublime
import sublime_plugin
import os
import re
import functools
import urllib2
import json

try:
    from functools import reduce
except:
    pass

class SnippetCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Called when the command is run."""
        self.edit = edit
        sublime.active_window().show_input_panel("Please enter your query:", "", self.on_text_done(), None, None)

    def on_text_done(self):
        def on_done(text):
            # call the method that returns the code snippets
            text = text.replace(' ', '%20')
            query = text
            text = 'http://recycle.cs.washington.edu:5000/search?query=' + text + '&token=cse504'
            f = urllib2.urlopen(text)
            choices = []
            data = json.load(f)
            print data
            for d in data:
                id = d.pop(0)
                code = d.pop()
                code = ' '.join(code)
                # code = code.replace('\n', ' ')
                choices.append(code)

            self.view.run_command('snippet_selection_helper', {
                'args': {
                    'choices': choices,
                    'query' : query
                }
            })

        return on_done


class SnippetSelectionHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):
        """Called when the command is run."""
        self.choices = args['choices']
        self.edit = edit
        self.query = args['query']

        self.selectify(self.choices)

        sublime.active_window().show_quick_panel(
            self.choices, self.on_done_call_func(args['choices']))

    def selectify(self, choices):
        tuples = [(idc, choice.split('\n')) for idc,choice in enumerate(choices)]
        self.mapping = reduce(lambda a,b:a+[None]+b, [[idc]*len(lines) for (idc,lines) in tuples])
        self.choices = reduce(lambda a,b:a+['--------------------------------']+b, [lines for (idc,lines) in tuples])

    def on_done_call_func(self, choices):
        """Return a function which is used with sublime list picking."""
        def on_done(index):
            if index >= 0 and self.mapping[index] is not None:
                return self.insert(choices[self.mapping[index]],self.mapping[index])

        return on_done

    def insert(self, choice, index):
        self.view.run_command('snippet_insert_helper', {
            'args': {
            #TODO: return choice to the learning algorithm
                'choice': choice,
                'index': index,
                'query': self.query
            }
        })

class SnippetInsertHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):
        choice = args['choice']
        content = choice
        position = self.view.sel()[0].begin()
        self.view.insert(edit, position, content)

        urllib2.urlopen('http://recycle.cs.washington.edu:5000/feedback?query='+args['query']+'&token=cse504&docid='+str(args['index']))
