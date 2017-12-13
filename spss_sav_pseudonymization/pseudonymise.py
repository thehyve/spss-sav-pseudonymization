#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# :noTabs=true:
# (c) Copyright (c) 2017  The Hyve
"""
pseudonymise.py

Brief: replaces numbers in a given SAV file with a randomly chosen
numbers using UUID randomizer.

Author: Jochem Bijlard <jochem@thehyve.nl>

"""

import savReaderWriter
from uuid import uuid4
import click


@click.command()
@click.argument('input_file', type=str)
@click.option('-c', '--columns', type=str, default=None)
@click.option('-n', '--names', type=str, default=None)
@click.option('-o', '--output-file', type=str, help='Output file for the pseudonymised sav.')
@click.option('-m', '--mapping-file', type=str, help='Reuse a previously generated mapping file.')
@click.version_option(version='Pseudonymizer for SPSS SAV files.')
def pseudonymise(input_file: str,
                 columns: str = None,
                 names: str = None,
                 mapping_file: str = None,
                 output_file: str = None):
    """
    Create UUID integer for certain columns of an SAV file. If no columns are selected (either by name  '-n' or by
    number '-c') then automatically the first column is selected for pseudonymisation.

    :param input_file: points to input SAV file.
    :param columns: columns by number to pseudonymise, can be comma separated list (e.g. 0,5,7).
    :param names: columns by name to pseudonymise. Comma separated list (e.g. 'PIDnumber,PIDnumberRelation,OtherPID')
    :param mapping_file: file with a previously created mapping. Reuses the pseudonymisation
        and adds mappings for new numbers.
    :param output_file: path to output file, defaults to same directory as input sav with
        suffix '-pseudonymised.sav'.
    """

    uuid_map = {}
    if mapping_file:
        click.echo('Using uuid map: {}'.format(mapping_file))
        with open(mapping_file, 'r') as f:
            for line in f.readlines():
                if not line:
                    continue
                fis, uuid = line.strip().split('\t')
                uuid_map[fis] = uuid

    if output_file is None:
        output_file = input_file.rsplit('.', 1)[0] + '-pseudonymised.sav'

    output_map = input_file.rsplit('.', 1)[0] + '-mapping.tsv'

    with savReaderWriter.SavReader(input_file) as reader:

        int_columns = []
        header = [c.decode() for c in reader.getHeader(None)]

        if columns is not None:
            int_columns += [int(c) for c in columns.split(',') if c != '']

        if names is not None:
            for name in names.split(','):
                try:
                    idx = header.index(name)
                except ValueError:
                    raise SystemExit("Column {} not found in file. Aborting.".format(name))
                int_columns.append(idx)

        if not int_columns:
            int_columns = [0]

        click.echo("Pseudonymising columns: {!r}".format([header[c] for c in int_columns]))

        with savReaderWriter.SavWriter(
                savFileName=output_file,
                varNames=reader.varNames,
                varTypes=reader.varTypes,
                valueLabels=reader.valueLabels,
                varLabels=reader.varLabels,
                formats=reader.formats,
                missingValues=reader.missingValues,
                measureLevels=reader.measureLevels,
                columnWidths=reader.columnWidths,
                alignments=reader.alignments,
                varSets=reader.varSets,
                varRoles=reader.varRoles,
                varAttributes=reader.varAttributes,
                fileAttributes=reader.fileAttributes,
                fileLabel=reader.fileLabel,
                multRespDefs=reader.multRespDefs,
                caseWeightVar=reader.caseWeightVar) as writer:

            for record in list(reader):
                for n in int_columns:

                    # Safer to convert to string, as this is how the map would be
                    # read from file if it is used another time.
                    fis = str(record[n])
                    if fis not in uuid_map:
                        uuid_map[fis] = uuid4().int

                    record[n] = uuid_map[fis]

                writer.writerow(record)
            click.echo('Writing pseudonymised sav: {}'.format(output_file))

    # write uuid map to disk
    with open(output_map, 'w') as f:
        click.echo('Writing mapping file: {}'.format(output_map))
        for fis, uuid in uuid_map.items():
            f.write('{}\t{}\n'.format(fis, uuid))
    click.echo('Finished. Good bye.')


if __name__ == '__main__':
    pseudonymise()
