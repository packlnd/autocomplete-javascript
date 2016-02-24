import sublime
import sublime_plugin
import os
import re
import functools

class SnippetCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        """Called when the command is run."""
        self.edit = edit
        sublime.active_window().show_input_panel("Please enter your query:", "", self.on_text_done(), None, None)

    def on_text_done(self):
        def on_done(text):
            # call the method that returns the code snippets
            choices = ['a', 'b', 'c']
            
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
                'choice': choice
            }
        })

class SnippetInsertHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):
        choice = args['choice']
        content = choice 
        position = self.view.sel()[0].begin()
        self.view.insert(edit, position, content)