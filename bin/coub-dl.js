#!/usr/bin/env node

const Coub = require('../')
const { version } = require('../package')

// CLI Setup
const program = require('commander')
  .version(version)
  .option('-i, --input <input>', 'Input (coub link or id).')
  .option('-o, --output <output>', 'Output file location.')
  .option(
    '-c, --crop [crop]',
    'Crop the output (width:height:x_offset:y_offset).'
  )
  .option('-s, --scale <size>', 'Resize the output (widthxheight).')
  .option('-A, --no-audio', 'Prevent addition of audio to the output.')
  .option('-l, --loop <times>', 'Loop the coub X times,')
  .option(
    '-t, --time <amount>',
    'Set the maximal amount of seconds for the length of the output.'
  )
  .option(
    '-i, --info',
    'Use in order to view the logs from ffmpeg while it works.'
  )

program.on('--help', () => {
  const examples = [
    '\n  Examples:\n',
    '    coub-dl --input https://coub.com/view/135nqc --no-audio --output out.mp4',
    '    coub-dl -i https://coub.com/view/135nqc -o out.gif --crop --scale 250',
    '    coub-dl -i https://coub.com/view/135nqc -o out.mp4 --loop 3',
    '    coub-dl -i https://coub.com/view/135nqc -o out.mp4 --loop 10 --time 12'
  ].join('\n')

  console.log(examples)
})

program.parse(process.argv)

// Main
async function run() {
  const { input, output } = program
  if (!input || !output) {
    return console.log(
      'Please specify both input and output. Use --help to see the list of options.'
    )
  }

  const coub = await Coub.fetch(input)
  if (!coub) {
    return console.log(
      'Couldn\'t fetch your coub. Please check the url/id and try again.'
    )
  }

  if (program.loop) coub.loop(program.loop)
  if (program.audio) coub.attachAudio()
  if (program.crop) coub.crop(program.crop)
  if (program.scale) coub.scale(program.scale)
  if (program.time) coub.addOption('-t', program.time)
  if (program.info) coub.on('info', console.log)
  if (!program.crop && !program.scale) coub.addOption('-c', 'copy')
  coub.addOption('-shortest')

  return coub.write(output)
}

run()
