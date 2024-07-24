import os
import json
import logging
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective

# Configure logging
logging.basicConfig(filename='teams_extension.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class TeamsDirective(SphinxDirective):
    has_content = True
    required_arguments = 1  # Expect one argument: the path to the JSON file

    def run(self):
        # Get the path to the JSON file from the directive argument
        json_path = self.arguments[0]

        # Resolve the JSON file path relative to the source directory
        json_path = os.path.abspath(os.path.join(self.env.srcdir, json_path))

        # Log the JSON path
        logging.debug(f"JSON path: {json_path}")

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
                    print("Poster found")
    
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

def setup(app):
    app.add_directive('teams', TeamsDirective)
