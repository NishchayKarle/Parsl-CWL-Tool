class: CommandLineTool
cwlVersion: v1.0
baseCommand: echo

inputs:
  message:
    type: string
    inputBinding:
      position: 1

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr