import os
import json
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from PIL import Image

# Debug output
debug_output = False

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
                    resized_image_dir = "_static/images/resized"
                    resized_image_suffix = "_resized"
                    image_dir, image_name = os.path.split(image_path)
                    image_name, image_ext = os.path.splitext(image_name)
                    resized_image_path = f"{resized_image_dir}/{image_name}{resized_image_suffix}{image_ext}"
                    abs_resized_image_path = os.path.abspath(os.path.join(self.env.srcdir, resized_image_path))

                    if resize_image(abs_image_path,abs_resized_image_path,250) != None:
                        content.append(f"  .. image:: /{resized_image_path}")
                        # Path to full size image won't be working when run locally, but is working through GitHub pages
                        # Need to find a better solution in the future
                        # TO DO
                        content.append(f"    :target: /onstage/{image_path}")
                        content.append( "    :align: left")
                        content.append( "    :height: 250\n")

                if team.get('country'):
                    content.append(f"  {team['country']}\n")
                
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

        write_debug_output(rst_content)

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

                content.append(f":{award['name']}: :ref:`teams_{id}_{team_label}` ({get_team_country(award['team'],data)})")
                content.append( "\n")

        # Parse the generated content as reStructuredText
        rst_content = "\n".join(content)

        write_debug_output(rst_content)

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

                if superteam.get('introduction'):
                    content.append(f"  `Introduction <{superteam['introduction']}>`__\n")

                if superteam.get('performance'):
                    content.append(f"  `Performance <{superteam['performance']}>`__\n")

                for team in superteam['teams']:
                    team_country = get_team_country(team, data)
                    team_label = team.replace(' ', '_')

                    extra_blanks = ""

                    if superteam.get('introduction') or superteam.get('performance'):
                        extra_blanks = "  "
                
                    content.append(f"  {extra_blanks}:ref:`teams_{id}_{team_label}` ({team_country})\n")
                

                content.append( "\n")

        # Parse the generated content as reStructuredText
        rst_content = "\n".join(content)

        write_debug_output(rst_content)

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

        write_debug_output(rst_content)

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

def resize_image(abs_input_image_path, abs_output_image_path, new_height):
    if abs_input_image_path.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')) and os.path.exists(abs_input_image_path):
            img = Image.open(abs_input_image_path)
            aspect_ratio = img.width / img.height
            new_width = int(new_height * aspect_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            abs_output_image_dir, x = os.path.split(abs_output_image_path)

            if not os.path.exists(abs_output_image_dir):
                os.mkdir(abs_output_image_dir,)

            img.save(abs_output_image_path)
            return abs_output_image_path
    else:
        print(f"File provided for resize_image is in wrong format or not available. (Filepath: {abs_input_image_path})")
        return None
    
def write_debug_output(content):
    if debug_output:
        base_filename = "output"
        counter = 1
        filename = f"{base_filename}_{counter}.rst"

        # Check if the file already exists and create a new filename if necessary
        while os.path.exists(filename):
            counter += 1
            filename = f"{base_filename}_{counter}.rst"

        # Write the content to the file
        with open(filename, "w") as file:
            file.write(content)

        print(f"DEBUG Content written to {filename}\n")
        return None

def setup(app):
    app.add_directive('teams', PopulateTeams)
    app.add_directive('awards', PopulateAwards)
    app.add_directive('superteams', PopulateSuperteams)
    app.add_directive('superteam_awards', PopulateSuperteamAwards)
