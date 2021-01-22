import json
import subprocess
import sys

git_log_command = ['git', 'log', '--format=%B%H--DELIM--']
git_describe_command = ['git', 'describe', '--long']

git_tag_command = ['git', 'tag', '-a']
git_stage_command = ['git', 'add', 'package.json', 'CHANGELOG.md']
git_commit_command = ['git', 'commit', '-m']

repo_url = 'https://github.com/BrandonGower-Winter/ABMECS/commit/'


def generate_changelog(version_type=2):
    vprocess = subprocess.Popen(git_describe_command,
                               stdout=subprocess.PIPE)

    tag = vprocess.communicate()[0].decode('UTF-8').split('-')[0]

    git_log_command.insert(2, tag + '..HEAD')

    process = subprocess.Popen(git_log_command,
                               stdout=subprocess.PIPE)

    stdout = process.communicate()

    commits = stdout[0].decode('UTF-8').split('--DELIM--\n')

    features = []
    performance = []
    fixes = []

    for commit in commits:
        try:
            msg, sha = commit.split('\n')

            if msg.startswith('feat:'):
                msg = msg.replace('feat:', '')
                features.append((msg, sha))
            elif msg.startswith('fix:'):
                msg = msg.replace('fix:', '')
                fixes.append((msg, sha))
            elif msg.startswith('perf:'):
                msg = msg.replace('perf:', '')
                performance.append((msg, sha))

        except ValueError:
            continue

    # Get Version Data
    with open('package.json') as json_file:
        data = json.load(json_file)
        version = adjust_version(data['version'].split('.'), version_type)

        return version, format_changelog_markdown(version, features, fixes, performance)


def adjust_version(version, version_type):
    if version_type == 0:
        return str(int(version[0]) + 1) + '.0.0'
    elif version_type == 1:
        return version[0] + '.' + str(int(version[1]) + 1) + '.0'
    else:
        return version[0] + '.' + version[1] + '.' + str(int(version[2]) + 1)


def format_changelog_markdown(version, features, fixes, performance):

    # Add Title
    changelog = '#Version: ' + version + '\n\n'

    # Add Features
    changelog += format_commits('Features', features)
    # Add Fixes
    changelog += format_commits('Fixes', fixes)
    # Add Performance
    changelog += format_commits('Performance', performance)

    return changelog


def format_commits(title, list_of_commits):
    content = ''
    if len(list_of_commits) > 0:
        content = '##' + title + ':\n\n'

        for commit in list_of_commits:
            content += '- ' + commit[0] + ' ([' + commit[1][0:6] + '](' + repo_url + commit[1] + '))\n'

    return content


if __name__ == '__main__':
    version, changelog = generate_changelog(int(sys.argv[1]))

    # Update version number in package file
    with open('package.json') as json_file:
        package_data = json.load(json_file)

    package_data['version'] = version

    with open('package.json', 'w+') as json_file:
        json_file.write(json.dumps(package_data, indent=4))

    # Write new changelog to CHANGELOG.md
    with open('CHANGELOG.md', 'w+') as changelog_file:
        changelog_file.write(changelog)

    # Stage CHANGELOG and package.json
    subprocess.Popen(git_stage_command).communicate()

    # Commit CHANGELOG and package.json
    git_commit_command.append('"auto: Created package data for version: ' + version + ' and generated the accompanying '
                                                                                      'CHANGELOG.md."')
    subprocess.Popen(git_commit_command).communicate()

    # Add version tag to tag command and run it
    git_tag_command.append('v' + version)
    subprocess.Popen(git_tag_command).communicate()
