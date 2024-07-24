import os
import json
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective

class PopulateTeams(SphinxDirective):
    has_content = True
    required_arguments = 2  # Expect two arguments: the path to the JSON file + an ID to make sure references are unique

    def run(self):
        # Get the path to the JSON file from the directive argument
        json_path = self.arguments[0]
        id = self.arguments[1]

        # Resolve the JSON file path relative to the source directory
        json_path = os.path.abspath(os.path.join(self.env.srcdir, json_path))

        # Load JSON data
        try:
            with open(json_path, 'r') as file:
                teams = json.load(file)
        except Exception as e:
            error = self.state_machine.reporter.error(
                f"Failed to load JSON file {json_path}: {str(e)}",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        # Container for the team information
        content = []

        for team in teams:
            if team.get('name'):
                team_label = team['name'].replace(' ', '_')

                content.append(f".. _teams_{id}_{team_label}:\n")

                content.append(f"{team['name']}")
                content.append( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                
                if team.get('image'):
                    content.append(f"  .. image:: {team['image']}")
                    content.append( "    :align: left")
                    content.append( "    :height: 250\n")

                if team.get('country'):
                    content.append(f"  {team['country']}\n")
    
                if team.get('poster'):
                    content.append(f"  `Poster <{team['poster']}>`_\n")
    
                if team.get('documentation'):
                    content.append(f"  `Documentation <{team['documentation']}>`_\n")
    
                if team.get('tdv'):
                    content.append(f"  `Technical Demonstration Video <{team['tdv']}>`_\n")
    
                if team.get('performance'):
                    content.append(f"  `Performance <{team['performance']}>`_\n")
                
                content.append( "\n")

        # Parse the generated content as reStructuredText
        rst_content = "\n".join(content)

        node = nodes.section()
        node.document = self.state.document
        self.state.nested_parse(
            self.state_machine.input_lines.__class__(rst_content.splitlines()),
            self.content_offset,
            node,
            match_titles=True
        )

        return node.children

class PopulateAwards(SphinxDirective):
    has_content = True
    required_arguments = 2  # Expect two arguments: the path to the JSON file + an ID to make sure references are unique

    def run(self):
        # Get the path to the JSON file from the directive argument
        json_path = self.arguments[0]
        id = self.arguments[1]

        # Resolve the JSON file path relative to the source directory
        json_path = os.path.abspath(os.path.join(self.env.srcdir, json_path))

        # Load JSON data
        try:
            with open(json_path, 'r') as file:
                awards = json.load(file)
        except Exception as e:
            error = self.state_machine.reporter.error(
                f"Failed to load JSON file {json_path}: {str(e)}",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        # Container for the team information
        content = []

        for award in awards:
            if award.get('name'):
                team_label = award['team'].replace(' ', '_')

                content.append(f"**{award['name']}:** :ref:`teams_{id}_{team_label}`")
                content.append( "\n")

        # Parse the generated content as reStructuredText
        rst_content = "\n".join(content)

        node = nodes.section()
        node.document = self.state.document
        self.state.nested_parse(
            self.state_machine.input_lines.__class__(rst_content.splitlines()),
            self.content_offset,
            node,
            match_titles=True
        )

        return node.children

def setup(app):
    app.add_directive('teams', PopulateTeams)
    app.add_directive('awards', PopulateAwards)
