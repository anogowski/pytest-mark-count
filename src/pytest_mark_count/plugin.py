#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

# Python Includes
from hmac import new
import logging
from dataclasses import dataclass
from typing import Any, Final, Generator, Iterable
from enum import StrEnum

# Pytest Includes
import pytest
from pytest import Item, MarkDecorator, TestReport, CollectReport
from pytest_metadata.plugin import metadata_key

from _pytest.mark import Mark
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from _pytest.config import Config, Notset
from _pytest.main import Session
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from _pytest.terminal import TerminalReporter
from _pytest.scope import Scope


def pytest_addoption(parser: Parser):
	group = parser.getgroup('mark-count')
	group.addoption('--count-marker', action='store', dest='count_markers', default=None, help="""Set markers to count (Space Delimited).\nWill automatically report unique tests.\nex: 'it vt'""")


def pytest_load_initial_conftests(early_config: Config, parser: Parser):
	mark_count_plugin: MarkCountPlugin = MarkCountPlugin(early_config)
	early_config.pluginmanager.register(mark_count_plugin)


@dataclass
class MarkData:
	_nodeid: Final[str]
	_markers: Final[list[str] | None]

	@property
	def nodeid(self) -> str:
		return self._nodeid

	@property
	def markers(self) -> list[str] | None:
		return self._markers

	@property
	def num_markers(self) -> int:
		num_markers: int = 0
		if self._markers is not None:
			num_markers = len(self._markers)
		return num_markers


class DefaultMarkers(StrEnum):
	MARKED = "marked"
	UNMARKED = "unmarked"
	UNIQUE = "unique"
	TOTAL = "total"


class MarkCountPlugin:

	_search_markers: list[str] | None = None
	_ini_markers: list[str] | None = None
	_markers_count: dict[str, int] = {}

	def __init__(self, config: Config):
		self.config = config
		self._markers_count[DefaultMarkers.MARKED] = 0
		self._markers_count[DefaultMarkers.UNMARKED] = 0
		self._markers_count[DefaultMarkers.UNIQUE] = 0
		self._markers_count[DefaultMarkers.TOTAL] = 0

		# self._ini_markers = self.config.inicfg.get("markers")

		temp_markers: Any = self.config.getoption("count_markers")

		if temp_markers is not None and isinstance(temp_markers, str):
			try:
				self._search_markers = temp_markers.split()
				for marker in self._search_markers:
					self._markers_count[marker] = 0
			except:
				logging.error("Please put the marker(s) in a space delimited list")

	@property
	def num_marked_tests(self) -> int:
		return self.query_markers_count(DefaultMarkers.MARKED)

	@property
	def num_unmarked_tests(self) -> int:
		return self.query_markers_count(DefaultMarkers.UNMARKED)

	@property
	def num_unique_marked_tests(self) -> int:
		return self.query_markers_count(DefaultMarkers.UNIQUE)

	@property
	def num_total_tests(self) -> int:
		return self.query_markers_count(DefaultMarkers.TOTAL)

	@property
	def markers_to_search_for(self) -> list[str] | None:
		return self._search_markers

	@property
	def mark_count_dict(self) -> dict[str, int]:
		return self._markers_count

	def pytest_itemcollected(self, item: Item) -> None:
		self._markers_count[DefaultMarkers.TOTAL] += 1
		if isinstance(self._search_markers, list) or isinstance(self._search_markers, str):
			item_markers: list[str] = [x.name for x in item.own_markers]

			if len(item_markers) > 0:
				self._markers_count[DefaultMarkers.MARKED] += 1
			else:
				self._markers_count[DefaultMarkers.UNMARKED] += 1

			intersection: set[str] = set(item_markers) & set(self._search_markers)
			if len(intersection) > 0:
				self._markers_count[DefaultMarkers.UNIQUE] += 1

			for name in intersection:
				self._markers_count[name] += 1

	def pytest_collection_finish(self, session: Session) -> None:
		...

	def query_markers_count(self, key: str | DefaultMarkers) -> int:
		return self._markers_count[key]

	def pytest_collectreport(self, report: CollectReport) -> None:
		new_sections: Iterable[tuple[str, str]] = []
		for key, value in self._markers_count.items():
			new_sections.append((key, str(value)))

		report.sections = report.sections + new_sections
