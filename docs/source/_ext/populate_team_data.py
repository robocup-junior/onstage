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
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            error = self.state_machine.reporter.error(
                f"Failed to load JSON file {json_path}: {str(e)}",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        # Container for the team information
        content = []

        for team in data['teams']:
            if team.get('name'):
                team_label = team['name'].replace(' ', '_')

                content.append(f".. _teams_{id}_{team_label}:\n")

                content.append(f"{team['name']}")
                content.append( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                
                image_path = team['image']
                abs_image_path = os.path.abspath(os.path.join(self.env.srcdir, image_path))

                if team.get('image') and os.path.exists(abs_image_path):
                    content.append(f"  .. image:: /{image_path}")
                    content.append( "    :align: left")
                    content.append( "    :height: 250\n")

                if team.get('poster'):
                    content.append(f"  `Poster <{team['poster']}>`__\n")
    
                if team.get('documentation'):
                    content.append(f"  `Documentation <{team['documentation']}>`__\n")
    
                if team.get('tdv'):
                    content.append(f"  `Technical Demonstration Video <{team['tdv']}>`__\n")
    
                if team.get('performance'):
                    content.append(f"  `Performance <{team['performance']}>`__\n")
                
                content.append( "\n")

        # Parse the generated content as reStructuredText
        rst_content = "\n".join(content)

        #To debug the output of the above commands:
        #
        # with open("output.rst", "w") as file:
        #    # Step 3: Write the content to the file
        #    file.write(rst_content)

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
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            error = self.state_machine.reporter.error(
                f"Failed to load JSON file {json_path}: {str(e)}",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        # Container for the team information
        content = []

        for award in data['awards']:
            if award.get('name'):
                team_label = award['team'].replace(' ', '_')

                content.append(f":{award['name']}: :ref:`teams_{id}_{team_label}`")
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

class PopulateSuperteams(SphinxDirective):
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
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            error = self.state_machine.reporter.error(
                f"Failed to load JSON file {json_path}: {str(e)}",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        # Container for the team information
        content = []

        for superteam in data['superteams']:
            if superteam.get('name'):
                team_label = superteam['name'].replace(' ', '_')

                content.append(f".. _superteams_{id}_{team_label}:\n")

                content.append(f"{superteam['name']}")
                content.append( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

                if superteam.get('performance'):
                    content.append(f"  `Performance <{superteam['performance']}>`__\n")

                for team in superteam['teams']:
                    team_country = get_team_country(team, data)
                    team_label = team.replace(' ', '_')

                    content.append(f"  :ref:`teams_{id}_{team_label}` ({team_country})\n")
                
                content.append( "\n")

        # Parse the generated content as reStructuredText
        rst_content = "\n".join(content)

        #To debug the output of the above commands:
        #
        # with open("output.rst", "w") as file:
        #    # Step 3: Write the content to the file
        #    file.write(rst_content)

        node = nodes.section()
        node.document = self.state.document
        self.state.nested_parse(
            self.state_machine.input_lines.__class__(rst_content.splitlines()),
            self.content_offset,
            node,
            match_titles=True
        )

        return node.children

class PopulateSuperteamAwards(SphinxDirective):
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
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            error = self.state_machine.reporter.error(
                f"Failed to load JSON file {json_path}: {str(e)}",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        # Container for the team information
        content = []

        for award in data['superteam_awards']:
            if award.get('name'):
                team_label = award['superteam'].replace(' ', '_')

                content.append(f":{award['name']}: :ref:`superteams_{id}_{team_label}`")
                content.append( "\n")
            else:
                print("NO                     AWARD\n")
                print(award)

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

def get_team_country(team_name, data):
    for team in data["teams"]:
        if team["name"] == team_name:
            return team["country"]
    return None

def setup(app):
    app.add_directive('teams', PopulateTeams)
    app.add_directive('awards', PopulateAwards)
    app.add_directive('superteams', PopulateSuperteams)
    app.add_directive('superteam_awards', PopulateSuperteamAwards)
