import sublime
import sublime_plugin
import os
import re
import functools
import urllib2
import json

class SnippetCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        """Called when the command is run."""
        self.edit = edit
        sublime.active_window().show_input_panel("Please enter your query:", "", self.on_text_done(), None, None)

    def on_text_done(self):
        def on_done(text):
            # call the method that returns the code snippets
            text = text.replace(' ', '%20')
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
                    'choices': choices
                }
            })

        return on_done
        

class SnippetSelectionHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):
        """Called when the command is run."""
        self.choices = args['choices']
        self.edit = edit

        sublime.active_window().show_quick_panel(
            self.choices, self.on_done_call_func(self.choices))

    def on_done_call_func(self, choices):
        """Return a function which is used with sublime list picking."""
        def on_done(index):
            if index >= 0:
                return self.insert(choices[index])

        return on_done

    def insert(self, choice):
        self.view.run_command('snippet_insert_helper', {
            'args': {
            #TODO: return choice to the learning algorithm
                'choice': choice
            }
        })

class SnippetInsertHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):
        choice = args['choice']
        content = choice 
        position = self.view.sel()[0].begin()
        self.view.insert(edit, position, content)